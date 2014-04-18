$(document).live('ready', function(){
        function getSortableArr(){
                var arr = $(".sortable").sortable('toArray')
                var t = ''
                clear_arr = $.map( arr, function(n){
                  if (n!='no_sortable') {

                    return n
                  }
                });
                  jQuery.each(clear_arr, function(i, val) {
                      if (i==clear_arr.length-1) {
                        t = t + val
                      }
                      else {
                        t = t + val + ','
                      }
                  });
                  $('#gallery').val(t);
            }
        $("form."+form_class).append('<textarea id="gallery" name="gallery" style="display: none;"></textarea>');
        $('label.img').toggle(
                function(){
                    $('.img_hide').fadeIn();
                    $(this).html('картинки (-)');
                },
                function(){
                    $('.img_hide').fadeOut();
                    $(this).html('картинки (+)');
                }

            );

            $('input.input_upload').change(function(){
                $('form.form_gallery').submit()
            })

            var bar = $('.bar');
            var percent = $('.percent');
            var status = $('#status');
            var gallery = $('.gallery');
               
            $('form.form_gallery').ajaxForm({
                beforeSend: function() {
                    //gallery.empty();
                    var percentVal = '0%';
                    bar.width(percentVal)
                    percent.html(percentVal);
                },
                uploadProgress: function(event, position, total, percentComplete) {
                    var percentVal = percentComplete + '%';
                    bar.width(percentVal)
                    percent.html(percentVal);
                    //console.log(percentVal, position, total);
                },
                // complete: function(xhr) {
                //     gallery.append(xhr.responseText);
                //     getSortableArr();
                //     ftooltipe();
                // },
                success: function(json) {
                  gallery.append(json.content);
                  getSortableArr();
                  // ftooltipe();
                }
            });

            $('form.detail_gallery').ajaxForm({
                delegation: true,
                beforeSend: function() {
                },
                complete: function(xhr) {
                }
            }); 

            $(".info_more_img").live("click", function() {
                var title = $(this).siblings('li').find('.title_more_img').val()
                var description = $(this).siblings('li').find('.description_more_img').val()
                var parent = $(this).parent('ul').parent('li.more_inf')
                var parent_id = $(this).parent('ul').parent('li.more_inf').attr('id')
                parent.attr('id', parent_id+'#36tghcn==more==36tghcn#'+title+'#36tghcn==more==36tghcn#'+description);
                getSortableArr()
                $(this).parent('ul').fadeOut()
            });

            $(".sortable").sortable({
              placeholder: "state-highlight",
              stop: function(event, ui) {
                getSortableArr()
              },
              start: function(event, ui) {
                $('.tooltipe').css('display', 'none');
              }
            });

    $(".aj_delete_hide_img").live("click", function(){
        var id = $(this).attr('id');
        var path = $(this).attr('path');
        var name = $(this).attr('name');
        if (path != 'recovery' && path != 'hide') {
            if (confirm("Удалить выбранное безвозвратно?")) {
                var dat = "confirm=yes&del_img_id="+id+"&del_img_path="+path+"&del_img_name="+name
            }
            else {
                var dat = "confirm=no&del_img_id="+id+"&del_img_path="+path+"&del_img_name="+name
            }
        }
        else {
            var dat = "confirm=yes&del_img_id="+id+"&del_img_path="+path+"&del_img_name="+name
        }
        $.ajax({
           type: "GET",
           url: url_aj_delete_hide_img,
           data: dat,
           success: function(msg){
             if ( msg == 'ok' ){
                cls = name.replace(/\s+/g,'-').replace(/[^a-zA-Z0-9\-]/g,'').toLowerCase();
                if (path == 'hide') {
                    $('img#'+cls).css('opacity', '0.3');
                    $('.cls_'+cls).attr('path', 'recovery');
                    $('.cls_'+cls).text('Восстановить');
                }
                else if (path == 'recovery') {
                    $('img#'+cls).css('opacity', '1');
                    $('.cls_'+cls).attr('path', 'hide');
                    $('.cls_'+cls).text('Скрыть');
                }
                else {
                        $('.im_'+cls).remove();
                }
                $('ul .dropdown-menu').css('display', 'none');
                getSortableArr()
             }
           }
         });
    });
    $(".aj_delete_hide_img_more").live("click", function(){
        var id = $(this).attr('id');
        var path = $(this).attr('path');
        var name = $(this).attr('name');
        if (path != 'recovery' && path != 'hide') {
            if (confirm("Удалить выбранное безвозвратно?")) {
                var dat = "confirm=yes&del_img_id="+id+"&del_img_path="+path+"&del_img_name="+name
            }
            else {
                var dat = "confirm=no&del_img_id="+id+"&del_img_path="+path+"&del_img_name="+name
            }
        }
        else {
            var dat = "confirm=yes&del_img_id="+id+"&del_img_path="+path+"&del_img_name="+name
        }
        $.ajax({
           type: "GET",
           url: "/dmn/aj_delete_hide_img/?more=true",
           data: dat,
           success: function(msg){
             if ( msg == 'ok' ){
                cls = name.replace(/\s+/g,'-').replace(/[^a-zA-Z0-9\-]/g,'').toLowerCase();
                if (path == 'hide') {
                    $('img#'+cls).css('opacity', '0.3');
                    $('.cls_'+cls).attr('path', 'recovery');
                    $('.cls_'+cls).text('Восстановить');
                }
                else if (path == 'recovery') {
                    $('img#'+cls).css('opacity', '1');
                    $('.cls_'+cls).attr('path', 'hide');
                    $('.cls_'+cls).text('Скрыть');
                }
                else {
                    $('.im_'+cls).remove();
                }
                $('ul .dropdown-menu').css('display', 'none');
                getSortableArr()
             }
           }
         });
    });


$('.detail_gallery').live("submit", function() { 
    $(".modal").modal('hide');
});
$(function(){
        getSortableArr();
        // allstat();
        })

      });