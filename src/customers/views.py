from django.template import RequestContext
from django.shortcuts import render_to_response 
from customers.models import CustomerForm, Customer, UserForm2
from django.contrib.auth.models import User

def editProfile(request):
    #currentUser=request.user #User.objects.get(username='testRAhim')
    
    customer=Customer.objects.get(user=request.user.id)
    userForm=UserForm2(instance = request.user)
    customerForm=CustomerForm(instance = customer)
    #    customerForm.fields['user'].widget.attrs['readonly'] = True
    return render_to_response('customers/edit_profile.html', 
                              {'user': request.user ,
                               'userForm':userForm ,  
                               'customerForm':customerForm },
                              context_instance=RequestContext(request))

def updateProfile(request):
    currentUser=User.objects.get(pk=request.user.id)
    c=Customer.objects.get(user=currentUser.id)
    customerForm=CustomerForm(request.POST, instance = c)
    
    userForm=UserForm2(request.POST, instance = currentUser)
    
    if customerForm.is_valid() and userForm.is_valid():
        customerForm.save()
        userForm.save()
        
    request.user = User.objects.get(pk=request.user.id)
    #customer=Customer.objects.get(user=request.user.id)
    #customerForm=CustomerForm(instance = customer)
    return render_to_response('customers/edit_profile.html',
                               {'user': request.user ,
                                'userForm':userForm , 
                                'customerForm':customerForm },
                               context_instance=RequestContext(request))