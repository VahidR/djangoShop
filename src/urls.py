from django.conf.urls.defaults import *
from customers.forms import UserRegistrationForm
from registration.views import register
import registration.backends.default.urls as regUrls
from django.views.generic.simple import direct_to_template
from customers import regbackend

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'djangoShop.products.views.home'),
    url(r'^accounts/editProfile/$', 'djangoShop.customers.views.editProfile'),
    url(r'^accounts/updateProfile/$', 'djangoShop.customers.views.updateProfile'),
    url(r'^return_url/$', 'djangoShop.products.views.home'),
    url(r'^cancel_url$', 'djangoShop.orders.views.get_cart'),
    url(r'^cart/addtocart/(?P<product_id>\d+)/$', 'djangoShop.orders.views.add_to_cart'),
    url(r'^cart/updateIteminCart/(?P<product_id>\d+)/$', 'djangoShop.orders.views.update_item_in_cart'),
    url(r'^cart/removeItem/(?P<product_id>\d+)/$', 'djangoShop.orders.views.remove_from_cart'),
    url(r'^product/search/$', 'djangoShop.products.views.search'),
    url(r'^product/category/(?P<category_id>\d+)$', 'djangoShop.products.views.show_category'),
    url(r'^product/(?P<product_id>\d+)/$', 'djangoShop.products.views.product_info'),
    (r'^cart/', include('cart.urls')),
    
    
    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    url(r'^accounts/register/$',
    register,
    {'backend': 'registration.backends.default.DefaultBackend','form_class':UserRegistrationForm},        
    name='registration_register'
    ),
    url('^accounts/profile/$', direct_to_template, {'template': 'profile.html'}, name="profile"),
    (r'^accounts/', include('registration.backends.default.urls')),
)


urlpatterns += staticfiles_urlpatterns()


