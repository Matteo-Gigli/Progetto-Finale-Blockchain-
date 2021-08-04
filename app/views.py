from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView
from .models import Item, Customer
from .mixins import StaffMixins
from .forms import MakeAnOffer
from django.contrib import messages
from django.urls import reverse
import redis

'''First of all we can import our Database.
We have to set it in our settings.py by CACHES and then we have to run the server from our Command-Prompt by 
redis-server.exe and then by redis-cli.exe'''

client = redis.StrictRedis(host='127.0.0.1', port='6379')


'''First we want to give the opportuniy to the admin, to create a section with all the conditions specified
in our models.
First we have to know who is an admin, and who is a customer.
For this we can add a file in app, called mixins.py (go there).
Import StaffMixins
Now we can create a class to create a section and, as argument we can pass the StaffMixins and a CreateView.

Definition CreateView from edit.py:

'View for creating a new object, with a response rendered by a template'

If we go deep in documentation we will see this is what we need, and we can use it.

'''
class Create_Section(StaffMixins, CreateView):
    model = Item
    fields = "name", "image", "description", "starting_price", "buy_now", "end_auction"
    template_name = 'create_section.html'
    success_url = '/homepage/'


'''Now we need to show the section.'''

def show_section(request, pk):
    item = get_object_or_404(Item, pk=pk)
    context = {'item': item}
    return render(request, 'show_section.html', context)


'''Now we want to add a function to find what we want in our site'''

def find_in_site(request):
    if 'q' in request.GET:
        querystring = request.GET.get('q')
        if len(querystring) == 0:
            return redirect('/find_in_site/')
        item = Item.objects.filter(name__icontains=querystring)
        context = {'item': item}
        return render(request, 'find_in_site.html', context)

    else:
        return render(request, 'find_in_site.html')


'''Now we have one of the most important part of our site.
We want to integrate a form to make an offer for an Item, so we have to create a forms.py file in app.(go there)
Import forms
This function must to control a lot of stuff, follow the # in the function to have an explain'''

def make_an_offer(request, pk):
    customer = Customer.objects.get(user=request.user)
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        form = MakeAnOffer(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = customer
            form.offer = form.offer

# First to Control: if forms offer is less than 0
            if form.offer < 0:
                messages.error(request, 'This Offer Cannot Be Updated, Because Is Lower Than 0 $')
                return redirect(reverse(make_an_offer, kwargs={'pk': item.pk}))


# Second to Control: if forms offer = buy now price and there is no offer yet transmit on ropsten
            if form.offer == item.buy_now:
                if customer.balance >= item.buy_now and item.offer == 0.0:
                    customer.balance = customer.balance - float(item.buy_now)
                    item.buyer = customer
                    customer.save()
                    messages.success(request, """Your offer is equal to Buy Now price. Congrats To Your Wonderfull Item Choise. Your Balance Now Is """ + str(
                                            customer.balance) + ' $')

# ROPSTEN Json Here because we want the transmission to ropsten if there is a winner
                    winner_data_offer_equal_buy_now_no_prev_offer = {
                        'Winner': item.buyer.user,
                        'Final Item Price': item.buy_now,
                        'Winner Balance': customer.balance,
                        'Item Image': item.image,
                        'Item Name': item.name,
                    }
                    #item.write_on_chain(winner_data_offer_equal_buy_now_no_prev_offer)
                    item.delete()
                    return redirect('/homepage/')



# Third to Control: if forms offer = buy now price and there is an offer already transmit on ropsten and give back the
# money to the previous user
                if customer.balance >= item.buy_now and item.offer > 0.0:
                    prev_buyer = item.buyer
                    prev_offer = item.offer
                    prev_buyer_balance = prev_buyer.balance + float(prev_offer)
                    customer.balance = customer.balance - float(form.offer)
                    item.buyer = customer
                    user = Customer.objects.get(user=prev_buyer.user, balance=prev_buyer.balance)
                    if user in Customer.objects.all():
                        user.balance = prev_buyer_balance
                        user.save()
                        customer.save()
                        item.save()
                        messages.success(request,
                                            """Your offer is equal to Buy Now price. Congrats To Your Wonderfull Item Choise. Your Balance Now Is """ + str(
                                                customer.balance) + ' $')
# ROPSTEN Here
                        winner_data_offer_equal_buy_now_with_prev_offer = {
                            'Winner': item.buyer,
                            'Final Item Price': item.buy_now,
                            'Winner Balance': customer.balance,
                            'Item Image': item.image,
                            'Item Name': item.name,
                            }
                        #item.write_on_chain(winner_data_offer_equal_buy_now_with_prev_offer)
                        item.delete()
                        return redirect('/homepage/')
                    else:
                        messages.error(request, '''You can't buy this item''')
                        return redirect('/accounts/login/')



# Fourth to Control: if offer is more than buy now price redirect to offer forms
            if form.offer > item.buy_now:
                messages.error(request, """You offer is out of range! Maximum offer is """ + str(item.buy_now) + " $ ")
                return redirect(reverse(make_an_offer, kwargs={'pk': item.pk}))



# Fifth to Control: Now we start to check the information about the offer, in fact before we analyzed
# all the case for a form offer less than 0, biger than buy now price, and case of offer equal to buy now price.
# Now we have to analyzed all the other case.


# First to Control: if user balance is more than starting price, item offer and more than 0:
            #if offer = 0 and form is more or equal to starting price and user balance is more than form

            if customer.balance >= float(item.starting_price) and customer.balance >= float(item.offer) and customer.balance > 0:
                if item.offer == 0.0 and form.offer >= item.starting_price and customer.balance > form.offer:
                    customer.balance = customer.balance - float(form.offer)
                    item.offer = form.offer
                    item.buyer = customer
                    item.save()
                    item.buyer.save()
                    customer.save()
# REDIS here because we want to check, from our database, information about active Auction
# Here we are saving only the first buyer of the active Auction
                    real_time_winners_no_prev_offer = {
                        'Real Time Winner': str(item.buyer.user),
                        'Best Item Offer': str(item.offer),
                        'Real Time Winner Balance': str(customer.balance),
                        'Item Image': str(item.image),
                        'Item Name': str(item.name),
                        }
                    client.set('real_time_winners_no_prev_offer ', str(real_time_winners_no_prev_offer))
                    messages.success(request, 'Offer Update Succesfully')
                    return redirect('/homepage/')

                if item.offer == 0.0 and form.offer <= item.starting_price:
                    messages.error(request, 'Your Offer Cannot Be Updated, Starting Price For this Auction Is ' + str(item.starting_price) + ' $')
                    return redirect(reverse(make_an_offer, kwargs={'pk': item.pk}))

                if item.offer == 0.0 and form.offer > item.starting_price and customer.balance < form.offer:
                    messages.error(request, 'Your Offer Cannot Be Updated, Because You Do Not Have Necessary Funds ')
                    return redirect(reverse(make_an_offer, kwargs={'pk': item.pk}))



# Second to Control:Connected to --- if user balance is more than starting price, item offer and more than 0:
                # In this case we have already an offer on the Item
                if item.offer > 0.0 and form.offer > item.offer:
                    prev_buyer = item.buyer
                    prev_offer = item.offer
                    prev_buyer_balance = prev_buyer.balance + float(prev_offer)

                    if customer.balance >= item.offer and customer.balance > 0 and customer.balance > form.offer:
                        try:
                            user = Customer.objects.get(user=prev_buyer.user, balance=prev_buyer.balance)
                            if user in Customer.objects.all():
                                user.balance = prev_buyer_balance
                                user.save()
                        except:
                            user = Customer.objects.get(user=prev_buyer.user, balance=prev_buyer.balance)
                            if user not in Customer.objects.all():
                                messages.error(request, "We can't update your offer")
                                return redirect('/accounts/login/')

                        customer.balance = customer.balance - float(form.offer)
                        item.offer = form.offer
                        item.buyer = customer
                        item.save()
                        customer.save()
                        user.save()

# REDIS Here bacuse we want to registrate what it's happening in our Active Auction.
# With this json we know in real time, all the information about every single auction
                        real_time_winners_with_prev_offer = {
                            'Real Time Winner': str(item.buyer.user),
                            'Best Item Offer': str(item.offer),
                            'Real Time Winner Balance': str(customer.balance),
                            'Item Image': str(item.image),
                            'Item Name': str(item.name),
                            'Prev User': str(prev_buyer.user),
                            'Prev User Balance': str(prev_buyer.balance),
                            'Prev Offer': str(prev_offer),
                            'User Balance After Better Offer For The Item': str(prev_buyer_balance)
                            }
                        client.set('real_time_winners_with_prev_offer', str(real_time_winners_with_prev_offer))
                        messages.success(request, 'Offer Update Succesfully')
                        return redirect('/homepage/')



                    if customer.balance >= item.offer and customer.balance < form.offer:
                        messages.error(request, "This Offer Cannot Be Updated Because You Do Not Have Necessary Funds To Do This Transaction")
                        return redirect(reverse(make_an_offer, kwargs={'pk': item.pk}))



                if item.offer > 0.0 and form.offer <= item.offer:
                    messages.error(request, 'This Offer Cannot Be Updated Because Last Offer Is ' + str(item.offer) + ' $')
                    return redirect(reverse(make_an_offer, kwargs={'pk': item.pk}))



            else:
                messages.error(request, "This Offer Cannot Be Updated Because You Do Not Have Necessary Funds To Do This Transaction")
                return redirect(reverse(make_an_offer, kwargs={'pk': item.pk}))


    else:
        form = MakeAnOffer()
        context = {'form': form}
        return render(request, 'make_an_offer.html', context)



'''Now we want to define a direct buy now function'''


def buy_now(request):
    customer = Customer.objects.get(user=request.user)
    for item in Item.objects.filter().order_by('-end_auction'):
        buy_now = item.buy_now
        if customer.balance >= buy_now:
            customer.balance = customer.balance - float(buy_now)
            messages.success(request, "Your Buy-Now Choise Had Success. Congrats To Your Wonderfull Item Choise. Your Balance Now Is " + str(customer.balance) + ' $')
            item.buyer = customer
            customer.save()

#ROPSTEN Here
            winner_buy_now = {
                'Winner': item.buyer,
                'Final Item Price': item.buy_now,
                'Winner Balance': customer.balance,
                'Item Image': item.image,
                'Item Name': item.name,
                }
            #item.write_on_chain(winner_buy_now)
            item.delete()
            return redirect('/homepage/')
        else:
            messages.error(request, "You Do Not Have Necessary Funds To Do This Transaction! We Are Sending You Back To The Offer Section !")
            return redirect('make_an_offer/')



