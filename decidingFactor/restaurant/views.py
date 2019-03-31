from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from restaurant.forms import SearchForm, SignUpForm
from restaurant import yelp
from restaurant import db_functions

import logging
import json
import random

logger = logging.getLogger(__name__)

HTTP_RETRIES = 3
TIMEOUT = 20
TOTAL_RESTAURANTS = 6
OFFSET = 50


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
            db_functions.save_search_form_info(request.user, city, terms)
            restaurants = _determine_selections(request.user, city, terms)
    else:
        form = SearchForm()

    return render(request, 'restaurant.html',
                  {'restaurants': restaurants, 'form': form})


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


def _determine_selections(user, location, terms):
    """
    Function that derermines the selections for the user by calling the needed
    functions to collected the needed data.

    Does the following:
        - gets users unique visit history
        - makes a call to yelp to get most relevant top 50
        - Calculates the yelp picks
        - Calculates final picks using users history

    :param str location: location where user is looking to find restaurants
    :param str terms: string user entered to search for restaurants

    :return: Dict final restaurants from yelp
    """
    visit_history = db_functions.get_user_visit_history(user)
    yelp_restaurants = _get_yelp_restaurants(location, terms)
    yelp_picks, yelp_restaurants = _calculate_yelp_picks(
        visit_history, yelp_restaurants, location, terms)
    selections = _calculate_picks(visit_history, yelp_picks, yelp_restaurants)

    return selections


def _get_yelp_restaurants(location, terms, offset=0):
    """
    Function to get and return the yelp businesses based on location and terms
    provided by the user.

    :param str location: location where user is looking to find restaurants
    :param str terms: string user entered to search for restaurants
    :param int offset: Skip X amount restuarants before beginning to return

    :return: Dict restaurants from yelp
    """
    try:
        response = yelp.find_businesses(location=location, term=terms,
                                        offset=offset)
        restaurants = json.loads(response.content.decode('utf-8'))
    except json.decoder.JSONDecodeError:
        restaurants = {}

    return restaurants.get('businesses', {})


def _calculate_yelp_picks(visit_history, yelp_restaurants, location, terms):
    """
    Logic for gathering the appropriate yelp suggestions.

    The base yelp picks, top 50, are passed in as to always provide a top 50
    in case they change. As long as the user has gone to 1 or more places it
    will provide that many new suggestions in order to compensate for the places
    that have already been visited. It also provides a constantly updated list
    of new restaurants as long as the user continually provides ratings.

    :param QuerySet visit_history: Places user has been to
    :param dict yelp_restaurants: Top 50 places Yelp suggests
    :param str location: location where user is looking to find restaurants
    :param str terms: string user entered to search for restaurants

    :return: Set final_picks from yelp
    :return: Dict yelp_restaurants updated with information of new restaurants
    """
    if visit_history.count():
        more_yelp_restaurants = _get_yelp_restaurants(location, terms,
                                                      visit_history.count())
        # Update existing dictionary to include new restaurants pulled down
        # But start from the end of list because that is where newst values
        # will be
        for restaurant in more_yelp_restaurants[-visit_history.count():]:
            yelp_restaurants.append((restaurant))

    # extract restaurant names from yelp restaurants
    yelp_places = [restaurant.get('name') for restaurant in yelp_restaurants]

    # extract names from restaurants you have already visted
    places_visited = [restaurant.get('name') for restaurant in visit_history]

    # get the unique set of restaurants from yelp that the user has not already
    # given a rating to/been to
    final_picks = set(yelp_places) - set(places_visited)

    return final_picks, yelp_restaurants


def _calculate_picks(visit_history, yelp_picks, yelp_restaurants):
    """
    Logic for determining the final restaurants to give the user. Will provide
    at least 2 places the user enjoyed and 2 restaurants they saved for a later
    time, provided they have at least 2 in the database. Based on numbers from
    the search history will determine how many yelp restaurants will be
    displayed. Only a total of 6 restaurants will be returned to user with the
    information about that restaurant

    :param QuerySet visit_history: Places user has been to
    :param set yelp_picks: 50 yelp restaurant names
    :param dict yelp_restaurants: Contains information of yelp restaurants

    :return: Dict final restaurants from yelp
    """
    history = {}
    # Sort out visit history into proper categories (maybe sql instead)
    for restaurant in visit_history:
        if not history.get(restaurant['visithistory__rating']):
            history[restaurant['visithistory__rating'].lower()] = [restaurant['name']]
        else:
            history[restaurant['visithistory__rating'].lower()].append(restaurant['name'])

    good_places = set(history.get('loved', [])) | set(history.get('liked', []))
    saved = set(history.get('saved', []))
    # Pick at least 2 from good places and saved
    picks = []
    if len(good_places) >= 2:
        picks += random.sample(good_places, 2)

    if len(saved) >= 2:
        picks += random.sample(saved, 2)

    yelp = random.sample(yelp_picks, TOTAL_RESTAURANTS - len(picks))
    final_picks = []
    for restaurant in yelp_restaurants:
        if restaurant['name'] in yelp:
            final_picks.append(restaurant)

    return final_picks
