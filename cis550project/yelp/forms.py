__author__ = 'erhanhu'
from django import forms
from django.contrib.auth.models import User
from yelp.models import Zipcode, UserProfile


class ZipcodeForm(forms.ModelForm):
    options = [
        ('Restaurants', 'Restaurants'),
        ('Shopping', 'Shopping'),
        ('Bars', 'Bars'),
        ('all_cat', 'Search All Categories')
        ]
    code = forms.CharField(max_length=6, help_text='Please enter a zipcode.')
    # MUST HAVE THE SAME NAME AS IN MODELS.PY ('code')
    cat = forms.ChoiceField(choices=options, widget=forms.RadioSelect())

    class Meta:
        model = Zipcode
        fields = ('code',)


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)


class UserProfileForm(forms.ModelForm):
    location_options = [
        ('NV', 'Las Vegas, NV'),
        ('NC', 'Charlotte, NC'),
        ('IL', 'Urbana-Champaign, IL'),
        ('PA', 'Pittsburgh, PA'),
        ('AZ', 'Phoenix, AZ'),
        ('WI', 'Madison, WI'),
    ]

    preference_options = [
        ('Restaurants', 'Restaurants'),
        ('Shopping', 'Shopping'),
        ('Bars', 'Bars'),
    ]
    location = forms.ChoiceField(choices=location_options, widget=forms.RadioSelect())
    preference = forms.ChoiceField(choices=preference_options, widget=forms.RadioSelect())

    class Meta:
        model = UserProfile
        fields = ('location', 'preference')