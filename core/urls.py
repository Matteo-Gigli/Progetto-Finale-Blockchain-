from django.urls import path
from .views import Homeview

'''Setting path for the Homeview.
Remember:
core/urls.py, app/urls.py are already registered in Auction/urls.py by include function.
Now we can start to setup all the stuff for : 
login,
logout,
password change form,
password reset complete,
password reset confirm,
password reset done,
password change done,
password reset email,
password reset form.

We have to create a new directory in the project called templates,and another directory in it, called registration.
registration will be the directory to manage all the stuff.

To use this directory we have to register a new urlpatterns in Auction/urls.py
That patterns is by default in django and is used to manage all this kind of things

Now after the creation of all the html files in registration we can move to app/views.py 
to start to create all the things we need in our site.'''

urlpatterns = [
    path('homepage/', Homeview.as_view(), name='homepage'),
]