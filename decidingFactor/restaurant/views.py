from django.shortcuts import render
import os
import requests

# Create your views here.
def index(request):

    access_info = get_access()
    if access_info:
        restaurants = make_api_call(access_info)
    else:
        print("ERROR: Could not obtain YELP access information")
        return

    print(len(restaurants['businesses']))
    return render(request, 'index.html', {'restaurants': restaurants['businesses']})


def get_access():
    token_url = os.getenv('YELP_HOST')

    payload = {'client_id': os.getenv('YELP_CLIENT'),
               'client_secret': os.getenv('YELP_SECRET')}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    if payload['client_id'] and payload['client_secret']:
        response = http_request(url=token_url, headers=headers,
                                payload=payload, request_type='POST')
        return response
    else:
        return None

def make_api_call(access_info):
    url = os.getenv('YELP_API_HOST')
    auth = "{} {}".format(access_info['token_type'],
                          access_info['access_token'])
    headers = {'Authorization': auth}
    payload = {'location': 19128, 'term': 'vegan'}
    response = http_request(url=os.getenv('YELP_API_HOST'), headers=headers,
                            payload=payload, request_type='GET')
    return response

def http_request(url, payload, headers, request_type):
    """This function is meant to be a generic in order to execute different
    types of HTTP requests. For now in this project, we only need a GET and
    POST in order to get information from YELP. Include type param if other
    requests are needed.

    If there is a payload it will be a POST otherwise GET is expected.

    """
    if request_type == 'POST':
        response = requests.post(url, headers=headers, data=payload)
    elif request_type == 'GET':
        response = requests.get(url, headers=headers, params=payload)
    else:
        print("UNEXPECTED REQUEST TYPE")

    try:
        status_code = response.status_code

        if status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
    except Exception as error:
        print("Error getting status code: {}".format(error))
