from restaurant.models import Location, SearchHistory, Restaurant, VisitHistory


RESTAURANTS = {'Blackbird Pizza': {'type': 'pizza',
                                   'price':'$',
                                   'rating': 'love'},
               'HipCityVedge': {'type': 'vegan',
                                'price':'$$',
                                'rating': 'love'},
               'Honest Toms': {'type': 'tacos',
                               'price':'$',
                               'rating': 'liked'},
               'QDoba': {'type': 'fast food',
                         'price':'$',
                         'rating': 'like'},
               'Asi Asi Cafe': {'type': 'Mexican',
                                'price':'$$',
                                'rating': 'Undecided'},
               'OuchMyWallet': {'type': 'vegan',
                                'price':'$$$',
                                'rating': 'hated' }}


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
