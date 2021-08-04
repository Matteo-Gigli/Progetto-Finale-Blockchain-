from django.contrib import admin
from .models import Customer, Item


'''We are registering our models here, the we have to create a superuser to be the admin of this project,
and have the opportunity to manage it. 

After this we can setup the registration, and we can do this in our accounts/forms.py app'''

admin.site.register([Customer, Item])
# Register your models here.
