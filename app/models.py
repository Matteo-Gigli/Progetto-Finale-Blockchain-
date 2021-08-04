from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from .utils import sendTransaction
import hashlib

'''We created our project(Auction) and all the app we need for that:

account: is the app for the registration,
app : is the main app for our project,
core : is the manage-app

First of all we can setup our models in 'app'.

We have two models:

Customer, Item.

We want to use an image field,so we have to install pillow by pip install pillow,
we need also of redis and djando-crispy-forms so we can install django-redis by pip install django-redis and
django-crispy-forms in the same way.
django-crispy-forms is to make a nice page.
django-crispy-forms must to be register as an app in settings.py


Now we want to register our models so we have to setup our admin.py'''

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.FloatField(default=0)



class Item(models.Model):
    name = models.CharField(max_length=35)
    image = models.ImageField(blank=True, null=True)
    description = models.TextField()
    starting_price = models.FloatField(default=0)
    buy_now = models.FloatField(default=0)
    end_auction = models.DateTimeField(auto_now_add=False)
    offer = models.FloatField(default=0)
    buyer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)
    #hash = models.CharField(max_length=32, default=None, null=True)
    #txId = models.CharField(max_length=66, default=None, null=True)

    def get_absolute_url(self):
        return reverse('show_section', kwargs={'pk': self.pk})

    def get_url(self):
        return reverse('make_an_offer', kwargs={'pk': self.pk})


    def write_on_chain(self):
        self.hash = hashlib.sha256(Item.encode('utf-8')).hexdigest()
        self.txId = sendTransaction(self.hash)
        self.save()



# Create your models here.

