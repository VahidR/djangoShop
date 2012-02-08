from django.db import models

class Product(models.Model):
    '''
    The ``Product`` model represents a particular item It contains 
    information about the product for sale, which is common to all 
    items in the stor. These include, for example, the item's price,
     manufacturer, an image or photo, a description, etc.
    '''
    category = models.ForeignKey('Category')
    name = models.CharField(max_length = 300)
    slug = models.SlugField(max_length = 150)
    description = models.TextField()
    photo = models.ImageField(upload_to = 'product_photo', blank = True)
    manufacturer = models.CharField(max_length = 300, blank = True)
    price = models.DecimalField(max_digits = 6, decimal_places = 2)
    

    def __unicode__(self):
        return u'%s' % self.name

    
    
class Category(models.Model):
    '''
    The ``Category`` model represents a category within a specific
    ``Catalog`` object. Categories contain a ForeignKey to their
    catalog, as well as an optional ForeignKey to another category
    that will serve as a parent category.
    '''
    parent = models.ForeignKey('self', blank = True, null = True,
                               related_name = 'children')
    name = models.CharField(max_length = 300)
    slug = models.SlugField(max_length = 150)
    description = models.TextField(blank = True)

    def __unicode__(self):
        if self.parent:
            return u'%s: %s' % (self.parent.name , self.name)
        return u'%s' % (self.name)    