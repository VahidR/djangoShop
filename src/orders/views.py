from django.template import RequestContext
from django.shortcuts import render_to_response

from cart import Cart
from cart import models
from products.models import Product
import uuid

#import simplejson
import logging
import sys
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from cart.forms import CheckoutForm
from cart.signals import pp_ipn
from cart.models import Item

def add_to_cart(request, product_id):
    message=""
    quantity = request.GET['quantity']
    if check_is_int(quantity):
        quantity=int(quantity)
        product = Product.objects.get(id=product_id)
#    quantity=form.quantity
        cart = Cart(request)
        cart.add(product, product.price, quantity)
        return render_to_response('cart/cart.html', dict(cart=Cart(request)), 
                                  context_instance=RequestContext(request))
    else:
        message="Please enter a positive integer for quantity !"
        all_products = Product.objects.all()
        return render_to_response('products/show_products.html', 
                              {'all_products':all_products , 
                               'user':request.user , 'message':message})

def remove_from_cart(request, product_id):
#    form = my_form(request.GET)
#    if form.is_valid():
    product = Product.objects.get(id=product_id)
    cart = Cart(request)
    cart.remove(product)
    return render_to_response('cart/cart.html', dict(cart=Cart(request)),
                                  context_instance=RequestContext(request))
    

def get_cart(request):
    return render_to_response('cart/cart.html', dict(cart=Cart(request)), context_instance=RequestContext(request))

def update_item_in_cart(request, product_id):
    message=""
    cart = Cart(request)
    quantity = request.GET['quantity']
    if check_is_int(quantity):
        quantity=int(quantity)
        product = Product.objects.get(id=product_id)
#    quantity=form.quantity
        cart.update(product, product.price, quantity)
        return render_to_response('cart/cart.html', dict(cart=Cart(request)), 
                                  context_instance=RequestContext(request))
    else:
        message="Please enter a positive integer for quantity !"
        return render_to_response('cart/cart.html', dict(cart=Cart(request),message=message), 
                                  context_instance=RequestContext(request))
        

@login_required
def checkout(request):
    template_name='cart/checkout.html'
    pp_urls=None
    model=None
    '''
    Renders a form ready to be submit to paypal. Passes PAYPAL_URL, which is
    taken from settings. Also passes total, which is the total amount
    of all the cart items
    '''
    if request.user.is_authenticated():
        cart_id=request.session.get('CART-ID')
#        print cart_id, request.user
        cartModel = models.Cart.objects.get(id=cart_id)
        cartModel.user=request.user
        cartModel.save()
#        cartModel=models.Cart.objects.get(user=request.user)
        cart=Cart(request)
        items = Item.objects.filter(cart=cartModel)
        if model:
            ct = ContentType.objects.get_for_model(model)
            items = items.filter(content_type=ct)
        form = CheckoutForm(items, pp_urls)
        total = cart.total()
    #    for item in items:
    #        total += item.amount
        return render_to_response(template_name,{
                "form":form,
                "PAYPAL_URL": settings.PAYPAL_URL,
                "total": total,
                },context_instance=RequestContext(request))
    else:
        print "An user is not registered"


from paypal.standard.ipn.signals import payment_was_successful
def my_payment_was_successful_handler(sender, **kwargs):
    print 'successful payment'

payment_was_successful.connect(my_payment_was_successful_handler)
def payment_successful(request):
    '''
    handles the "IPN" from paypal. That is, when there is a successful paypal
    transaction, paypal calls this url with some info. The most important
    value here is POST['custom'], which is a comma seperated list of CartItem
    ids (ending in ,) that have been paid for.
    
    sends a list of cart_items to cart.signals.pp_ipn
    '''
    logging.debug('handling paypal IPN:')
    if request.method == 'POST':
        logging.debug('is post')
        itemids = request.POST['custom'].split(',')
        logging.debug('itemids:')
        logging.debug(itemids)
        try:
            cart_items = Item.objects.in_bulk(itemids[:-1])
        except:
            logging.debug('item fail')
            logging.debug(sys.exc_info())
            raise
        logging.debug('cart items:')
        logging.debug(cart_items)
        logging.debug('sending signal')
        pp_ipn.send(sender=None, cart_items=cart_items)
        logging.debug('signal sent')
    return HttpResponse('OK')
        


def check_is_int(x):  
    if x.isdigit():
        if int(x) == float(x) and int(x) > 0:
            return True
    return False
