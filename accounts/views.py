from django.shortcuts import render, redirect
from .forms import Registration_Form
from django.contrib.auth.models import User
from app.models import Customer
import random
from django.contrib.auth import authenticate,login
from django.contrib import messages

'''We have to import our form from accounts/forms.py to use it.
This is a TEST so, we are assign a random balance to use all the functionality of our site.
After the setup we have to create the html form.
so we can go in accounts/templates and create the html form.

After the html we have to go in Auction/urls.py to connect the registration form. '''




def registration(request):
    if request.method == 'POST':
        form = Registration_Form(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            new_customer = Customer(
                user=user,
                balance=random.randrange(500,1500)
            )
            user.save()
            new_customer.save()
            user = authenticate(username=username, password=password)
            login(request,user)
            messages.success(request, 'Your Registration is confirmed! Welcome to ArkaNet')
            return redirect('homepage/')

    else:
        form = Registration_Form()
        context = {'form': form}
        return render(request,'registration_form.html', context)
