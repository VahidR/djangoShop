from django import forms
from registration.forms import RegistrationForm
from django.utils.translation import ugettext_lazy as _
from customers.models import Customer
#from profiles.models import UserProfile
from registration.models import RegistrationProfile

attrs_dict = { 'class': 'required' }

class UserRegistrationForm(RegistrationForm):
    '''
    A class to design a form to show fields to be filled by customer. 
    A customer attribute are belong to the following classes:
    User class (the built-in class) and Customer
    '''
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)
    phone_number = forms.IntegerField()
    address_line_1 = forms.CharField(widget=forms.TextInput(attrs=attrs_dict))
    address_line_2 = forms.CharField(widget=forms.TextInput(attrs=attrs_dict),required=False)
    address_line_3 = forms.CharField(widget=forms.TextInput(attrs=attrs_dict),required=False)
    city = forms.CharField(widget=forms.TextInput(attrs=attrs_dict))
    postalcode = forms.CharField(widget=forms.TextInput(attrs=attrs_dict))
    provice = forms.CharField(widget=forms.TextInput(attrs=attrs_dict),required=False)
    country = forms.CharField(widget=forms.TextInput(attrs=attrs_dict))