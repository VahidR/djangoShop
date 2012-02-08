

from unittest import TestCase
from django.test.client import Client 
from django.core import urlresolvers

from djangoShop.products.models import Product


import httplib


class NewUserTestCase(TestCase):
    fixtures = ['product']
    def setUp(self):
        self.client = Client()
    
    def test_view_home(self):
        """
        this mudule test whether the showProduct is work fine or not. 
        it test our website to know it can load products. 
        i.e. we want to ensure that users can, in fact, load our home page
        if every thing is OK it 'll show OK
        """
        home_url = urlresolvers.reverse('home')
        response = client.get(home_url)
        # check that we did get a response
        self.failUnless(response)
        # check that status code of response was success
        # (httplib.OK = 200)
        self.assertEqual(response.status_code, httplib.OK)
        

        def test_delete_all(self):
            for p in Product.objects.all():
                p.delete()
                # check that the data
            self.assertEqual(Product.objects.all().count(),0)

        def test_products_exist(self):
            self.assertTrue(Product.objects.all().count() > 0)
