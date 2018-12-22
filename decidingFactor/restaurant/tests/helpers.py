from restaurant.models import Restaurant, VisitHistory

from restaurant.views import _get_yelp_restaurants


RESTAURANTS = {'Blackbird Pizza': {'type': 'pizza',
                                   'price': '$',
                                   'rating': 'loved'},
               'HipCityVedge': {'type': 'vegan',
                                'price': '$$',
                                'rating': 'loved'},
               'Honest Toms': {'type': 'tacos',
                               'price': '$',
                               'rating': 'liked'},
               'QDoba': {'type': 'fast food',
                         'price': '$',
                         'rating': 'liked'},
               'Asi Asi Cafe': {'type': 'Mexican',
                                'price': '$$',
                                'rating': 'Undecided'},
               'OuchMyWallet': {'type': 'vegan',
                                'price': '$$$',
                                'rating': 'hated'}}


def create_visit_history(location, search, user):
    for name, info in RESTAURANTS.items():
        rest = Restaurant.objects.create(location_id=location,
                                         name=name,
                                         restaurant_type=info['type'],
                                         price=info['price'])
        VisitHistory.objects.create(user_id=user,
                                    search_id=search,
                                    restaurant_id=rest,
                                    rating=info['rating'])


def new_create_visit_history(location, terms, search, user, num=6):
    restaurants = _get_yelp_restaurants(location.city, terms)
    for i in range(0, num):
        rest = Restaurant.objects.create(
            location_id=location, name=restaurants[i].get('name'),
            restaurant_type=restaurants[i].get('type'),
            price=restaurants[i].get('price'))

        VisitHistory.objects.create(user_id=user,
                                    search_id=search,
                                    restaurant_id=rest,
                                    rating='loved')
