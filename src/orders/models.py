from django.db import models
from django.contrib.auth.models import User
from djangoShop.products.models import Product
from djangoShop.customers.models import Customer
from datetime import datetime


class Basket(models.Model):
    '''
    Model to store the information of the user's basket. It set up the relation between 
    the user and his/her items in the basket.
    '''
    date = models.DateTimeField(default = datetime.now)
    total_price = models.DecimalField(max_digits = 7, decimal_places = 2)
    comments = models.TextField(blank = True)
    
    products = models.ManyToManyField(Product , through = 'Item')
    customer = models.ForeignKey(Customer)
    
    def __unicode__(self):
        return u'%s <%s @ %s>' % (self.customer,
                                  self.total_price,
                                  self.date)
    
    
class Item(models.Model):
    '''
    The ``Item`` model represents information about a
    specific product ordered by a customer.
    '''
    basket = models.ForeignKey(Basket)
    product = models.ForeignKey(Product)
    
    unit_price = models.DecimalField(max_digits = 7, decimal_places = 2)
    total_price = models.DecimalField(max_digits = 7, decimal_places = 2)
    quantity = models.PositiveIntegerField()
    comments = models.TextField(blank = True)    
