from django.urls import path
from .views import Create_Section, show_section, find_in_site, make_an_offer, buy_now

urlpatterns = [
    path('create_section/', Create_Section.as_view(), name='create_section'),
    path('show_section/<int:pk>', show_section, name='show_section'),
    path('find_in_site', find_in_site, name='find_in_site'),
    path('make_an_offer/<int:pk>', make_an_offer, name='make_an_offer'),
    path('buy_now/', buy_now, name='buy_now'),
]