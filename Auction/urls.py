"""Auction URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from accounts.views import registration
from django.conf import settings
from django.conf.urls.static import static

'''We import the registration function and we pass it as homepage by "".
At the same time we want to import all the app to our projects so, we can use
include function to made it.

We setted up an image in our model for the Items, so we have to setup a directory in our project called media,
will be our media directory.

We have setup even the urlpatterns to accept the media so first we have to go in setting.py, to setup up a media_root,
and a media_url.

MEDIA_URL : is same of STATIC_URL, but for the media
MEDIA_ROOT : is where our media file will be served and we setup in project

Now we can add the urlpatterns for the media.

Now we can go in core/views were we will create our Homeview.'''

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', registration, name='registration'),
    path('', include('core.urls')),
    path('', include('app.urls')),

]

urlpatterns += [
    path("accounts/", include("django.contrib.auth.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
