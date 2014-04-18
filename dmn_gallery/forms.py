from django import forms
from dmn_gallery.models import Details


class DetailsForm(forms.ModelForm):

    class Meta:
        model = Details
        exclude = ('name', 'stored')
