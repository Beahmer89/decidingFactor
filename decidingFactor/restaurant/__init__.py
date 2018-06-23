import os

from restaurant.mixins.yelp import YelpClient

yelp = YelpClient(os.getenv('YELP_API_KEY'))
