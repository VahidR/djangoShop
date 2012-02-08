from django.template import RequestContext
from django.shortcuts import render_to_response , get_object_or_404
from products.models import Product,Category
from django.db.models import Q

def home(request):
    '''
    This function show the list of all product in the database. 
    '''
    all_products = Product.objects.all()
    all_categories=Category.objects.all()
    request.session["all_categories"] = all_categories
    return render_to_response('products/show_products.html', 
                              {'all_products':all_products , 
                               'all_categories':all_categories,
                               'user':request.user})
    
def show_category(request, category_id):
    '''
    This function is used to the list of the product in a specific category
    i.e. it shows product by category
    '''
    all_products = Product.objects.all()
    category=Category.objects.get(pk=category_id)
    all_products=all_products.filter(category=category)
    all_categories=Category.objects.all()
    request.session["all_categories"] = all_categories
    return render_to_response('products/show_products.html', 
                              {'all_products':all_products , 
                               'all_categories':all_categories,
                               'category_name':category.name,
                               'user':request.user})
        
def search(request):
    '''
    Search name, description and manufacture of the product databse to
    find product that match the keywords.
    If the keyword is made by combination of several words it will do
    the search by each split word and joind the result.
    '''
    q=request.GET.get("q")
    if q and q!= ' ':
        words=q.split()
        all_products=Product.objects.all()
        for word in words:
            all_products=all_products.filter(Q(name__icontains=word) |
                                             Q(description__icontains=word) |
                                             Q(manufacturer__icontains=word) )
            search_result=all_products
    else:
        search_result=''
        
    return render_to_response('products/search.html', 
                              {'search_result':search_result , 
                               'user':request.user,
                               'q':q})
    

import uuid
from django.core.urlresolvers import reverse
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm
#from products.models import Product

def product_info(request, product_id):
    product=get_object_or_404(Product, pk=product_id)
    
    return render_to_response('products/product_info.html', {
        'product' : product,
        'photoPath': settings.MEDIA_ROOT,
    }, RequestContext(request))

def product_detail(request, slug):
    '''
    It is a smaple funcation that could be used to send only one item to
    Paypal. it will send the information of the select  product to be paied
    in Paypal.
    '''
    product = get_object_or_404(Product, pk=slug)
    paypal = {
        'amount': product.price,
        'item_name': product.name,
        'item_number': product.slug,
        
        # PayPal wants a unique invoice ID
        'invoice': str(uuid.uuid1()), 
        
        # It'll be a good idea to setup a SITE_DOMAIN inside settings
        # so you don't need to hardcode these values.
        'return_url': settings.SITE_DOMAIN + 'return_url', #reverse('return_url'),
        'cancel_return': settings.SITE_DOMAIN + 'cancel_url', #reverse('cancel_url'),
    }
    form = PayPalPaymentsForm(initial=paypal)
    if settings.DEBUG:
        rendered_form = form.sandbox()
    else:
        rendered_form = form.render()
    return render_to_response('products/product_detail.html', {
        'product' : product,
        'form' : rendered_form,
    }, RequestContext(request))