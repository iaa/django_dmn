import os
import hashlib
from json import JSONEncoder
from dmn_utils.spizz.pytils.translit import iaaslugify


def upload_file_to(files=None, path=None, max_size=0, encoding='utf-8'):
    error = {}
    files_error = {}

    if not files:
        error.update({'error': 'No file to upload'})
    if not path:
        error.update({'error': 'Invalid parameters'})
    if error:
        return JSONEncoder().encode(error)

    dst_file = None
    total_file = 0
    cur_size = 0
    max_size = int(max_size) * 1024 * 1024

    for file in files[0][1]:
        if (file.size <= max_size) and ((cur_size + file.size) <= max_size):
            fname = iaaslugify(file.name)
            file_path = os.path.join(path, fname.encode(encoding))

            try:
                dst_file = open(file_path, mode='wb+')
                for chunk in file.chunks():
                    dst_file.write(chunk)
                cur_size += file.size
                total_file += 1
            except IOError:
                if not total_file:
                    error.update({'error': 'Unable to upload files'})
                else:
                    error.update({'error': 'Some file was not uploaded'})
                    files_error.update({fname: 'Unable to save uploaded file'})
                    error.update({'errorData': files_error})
            finally:
                if dst_file is not None:
                    dst_file.close()
        else:

            if not total_file:
                error.update({'error': 'Unable to upload files'})
            else:
                error.update({'error': 'Some files was not uploaded'})
                files_error.update({fname: 'File exceeds the maximum allowed filesize'})
                error.update({'errorData': files_error})
            break

    return JSONEncoder().encode(error)


def find_dir(fhash, root_dir, path=None):
    """Find directory by hash"""
    fhash = str(fhash)
    if not path:
        path = root_dir
        if fhash == hash(path):
            return path

    if not os.path.isdir(path):
        return None

    for d in os.listdir(path):
        pd = os.path.join(path, d)
        if os.path.isdir(pd) and not os.path.islink(pd):
            if fhash == hash(pd):
                return pd
            else:
                ret = find_dir(fhash, pd)
                if ret:
                    return ret
    return None


def hash(path):
    """Hash of the path"""
    m = hashlib.md5()
    m.update(path)
    return str(m.hexdigest())
