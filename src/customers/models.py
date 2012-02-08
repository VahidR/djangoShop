from django.db import models
from django.contrib.auth.models import User
from django.contrib.localflavor.us.models import PhoneNumberField
from django.forms import ModelForm
from django import forms

class Customer(models.Model):
    '''
    The ``Customer`` model represents a customer of the online
    shop. It uses Django's built-in ``auth.User`` model, which
    contains information like first and last name, and email, and adds
    phone number and address information.
    '''
    user = models.OneToOneField(User)
    phone_number = PhoneNumberField(blank = True , null = True)
    address_line_1 = models.CharField(max_length = 300)
    address_line_2 = models.CharField(max_length = 300 , blank = True)
    address_line_3 = models.CharField(max_length = 300 , blank = True)
    city = models.CharField(max_length = 150)
    postalcode = models.CharField(max_length = 10)
    provice = models.CharField(max_length = 50 , blank = True , null = True)
    country = models.CharField(max_length = 150)
    
    def __unicode__(self):
        return u'%s ' % (self.user.username)
    
    
class CustomerForm(ModelForm):
    
    class Meta:
        model = Customer
        exclude = ('user',)
        
class UserForm2(ModelForm):
    # the sample code to make username field uneditable(i.e user can only see but cann't edit)
#    def __init__(self, *args, **kwargs):
#        super(UserForm2, self).__init__(*args, **kwargs)
#        instance = getattr(self, 'instance', None)
#        if instance.id:
#            self.fields['username'].widget.attrs['disabled'] = 'disabled'
#    
    
    class Meta:
        model = User
        fields=('first_name','last_name',)
#        exclude = []
#        for field_name in User.__dict__:
#            if field_name !='first_name' and field_name != 'last_name':
#                exclude.append(field_name)
                
class CustomerAddress(models.Model):
    '''
    The ``CustomerAddress`` model represents a customer's address. 
    '''
    pass
    
    
