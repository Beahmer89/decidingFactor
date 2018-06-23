from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from restaurant.forms import SearchForm, SignUpForm

import logging
import os
import requests

logger = logging.getLogger(__name__)

HTTP_RETRIES = 3
TIMEOUT = 20


# Create your views here.
def index(request):
    return render(request, 'index.html')


def restaurant(request):
    restaurants = {}
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            terms = form.cleaned_data.get('terms')
            city = form.cleaned_data.get('city')
    else:
        form = SearchForm()

    return render(request, 'restaurant.html',
                  {'restaurants': restaurants.get('businesses'), 'form': form})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def _get_restaurants(location, terms):
    pass
