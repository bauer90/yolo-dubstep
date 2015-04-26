__author__ = 'erhanhu'
from django import forms
from yelp.models import Zipcode


class ZipcodeForm(forms.ModelForm):
    options = [
        ('Restaurants', 'Restaurants'),
        ('Hotels', 'Hotels'),
        ('Bars', 'Bars'),
        ('all_cat', 'Search All Categories')
        ]
    code = forms.CharField(max_length=6, help_text='Please enter a zipcode.')
    # MUST HAVE THE SAME NAME AS IN MODELS.PY ('code')
    cat = forms.ChoiceField(choices=options, widget=forms.RadioSelect())

    class Meta:
        model = Zipcode
        fields = ('code',)
