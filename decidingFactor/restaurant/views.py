from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from restaurant.forms import SignUpForm

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
    restaurants = _make_api_call()
    return render(request, 'restaurant.html',
                  {'restaurants': restaurants['businesses']})


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


def _make_api_call():
    """ Setup the request needed to be made for YELP to get information"""
    auth = "bearer {}".format(os.environ.get('YELP_API_KEY'))
    headers = {'Authorization': auth}
    # hard coded for now until page gets working
    query_params = {'location': 19128, 'term': 'vegan'}
    response = http_request(url=os.getenv('YELP_API_HOST'), headers=headers,
                            query_params=query_params)
    return response


def http_request(url, headers, query_params={}, body={}, request_type='GET'):
    """This function is meant to be a generic in order to execute different
    types of HTTP requests. For now in this project, we only need a GET in
    order to get information from YELP. Include type param if other
    requests are needed.

    """
    for x in range(0, HTTP_RETRIES):
        response = requests.request(request_type, url,
                                    params=query_params, headers=headers,
                                    data=body, timeout=TIMEOUT)
        if 200 <= response.status_code < 400:
            return response.json()
        elif response.status_code in [423, 429]:
            logger.error('Rate limited')
        elif 400 <= response.status_code < 500:
            logger.error('400 level error: {}'.format(response.reason()))
            response.raise_for_status()
        elif response.status_code >= 500:
            logger.error('500 level error: {}'.format(response.reason()))

    # Raise final error
