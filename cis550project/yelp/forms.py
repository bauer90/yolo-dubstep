__author__ = 'erhanhu'
from django import forms
from yelp.models import Zipcode


class ZipcodeForm(forms.ModelForm):
    code = forms.CharField(max_length=6, help_text='Please enter a zipcode.')
    # MUST HAVE THE SAME NAME AS IN MODELS.PY ('code')

    class Meta:
        model = Zipcode
        fields = ('code',)
