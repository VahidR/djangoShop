'''
A sample function that get the user creation signal to save the additional information
of tghe customer along with the auth.User. 
'''
from customers import forms
from django.contrib.auth.models import User

def user_created(sender, user, request, **kwargs):
    form = forms.UserRegistrationForm(request.POST)
    new_user = User.objects.get(pk=user.id)
    new_user.is_active = False
    new_user.first_name=form.data['first_name']
    new_user.last_name=form.data['last_name']
    data = forms.Customer(user=user)
    data.phone_number = form.data["phone_number"]
    data.address_line_1 = form.data["address_line_1"]
    data.address_line_2 = form.data["address_line_2"]
    data.address_line_3 = form.data["address_line_3"]
    data.city = form.data["city"]
    data.postalcode = form.data["postalcode"]
    data.provice = form.data["provice"]
    data.country=form.data["country"]     
    data.city = form.data["city"]
    data.save()
    new_user.save()
    
from registration.signals import user_registered
user_registered.connect(user_created)