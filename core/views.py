from django.views.generic import ListView
from app.models import Item, Customer
from django.utils import timezone


'''We are creating here our Homeview.
First of all we define our Homevies as a ListView.

ListView Definition from list.py: 

Render some list of objects, set by `self.model` or `self.queryset`.
self.queryset` can actually be any iterable of items, not just a queryset.

So we can use it fou our Auction Site, in fact our Homepage will be a list of Items orderd by
"-end auction timing"

We are setting a queryset because is an iterable so we can use it later for the Item.

Now we create urls.py in core to set the Homeview as a path.
'''


class Homeview(ListView):
    queryset = Item.objects.all().order_by('-end_auction')
    template_name = 'homepage.html'
    for item in queryset:
        if timezone.now() >= item.end_auction and item.offer == 0.0:
            no_winner_data_for_ended_auction = {
                'Winner': item.buyer,
                'Starting Item Price': item.starting_price,
                'Item Image': item.image,
                'Item Name': item.name,
            }
            item.delete()

        if timezone.now() >= item.end_auction and item.offer > 0.0:
            winner_data_for_ended_auction = {
                'Winner': item.buyer,
                'Final Item Price': item.offer,
                'Winner Balance': item.buyer.balance,
                'Item Image': item.image,
                'Item Name': item.name,
            }
            item.delete()
