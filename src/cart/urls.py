from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    url(r'^checkout/$', 'orders.views.checkout', name="cart_checkout"),
    url(r'^success/', direct_to_template, {'template':'cart/success.html'}, name="cart_win"),
    url(r'^cancel/', direct_to_template, {'template':'cart/cancel.html'}, name="cart_cancel"),
    url(r'^ipn/$', 'orders.views.payment_successful', name="cart_ipn"),
)
