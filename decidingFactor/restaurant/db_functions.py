import datetime

from django import db

from restaurant import models


def save_search_form_info(user_id, search_location, terms):
    """
    Saves the search information that was used entered at the restaurant search
    page. If the location has not already been saved in the DB, it will be
    created in this fuction.

    :param int user_id: logged in user id
    :param str search_location: the area in which user is searching
    :param str terms: string user entered to search for restaurants

    :return: Dict of location object and search object
    """
    location, created = models.Location.objects.get_or_create(
        city=search_location)

    search, created = models.SearchHistory.objects.get_or_create(
        user_id=user_id, location_id=location, search_terms=terms)

    return {'location': location, 'search': search}


def save_restaurant_selection(name, location_id, price, restaurant_type):
    """
    Adds the given restaurant to the database.

    :param str location_id: location uuid of where restaurant is located
    :param str name: The name of the restaurant
    :param str price: Money signs indicating price range
    :param str restaurant_type: Category of restaurant

    :return: Restaurant object or None
    """
    try:
        restaurant, created = models.Restaurant.objects.get_or_create(
            name=name,
            location_id=location_id,
            restaurant_type=restaurant_type,
            price=price)
    except db.IntegrityError as error:
        return None

    return restaurant


def get_user_visit_history(user_id):
    """
    Retrieves a users visit history. Includes all places regardless of rating.

    :param int user_id: logged in user id

    :return: VisitHistory object
    """
    return models.Restaurant.objects.filter(
        visithistory__user_id=user_id).values(
            'restaurant_type', 'name', 'price', 'visithistory__rating',
            'visithistory__last_visited').distinct()


def save_visit_selection(user_id, search_id, restaurant_id, rating):
    """
    Record the users choice on a particular restaurant. This function handles
    the initial user selection of restaurants. The user can pick from the
    following:
        - They are going to the restaurnat
        - Do not like the place
        - Like the place, but will save it for another time

    If a selection that does not equal any of the specified ratings,
    the request is ignored. Other wise a boolean response is returned
    indicating whether the record was created.

    :param str user_id: UUID of user
    :param str restaurant_id: UUID of restaurant
    :param str search_id: UUID of search user entered to find these results
    :param str rating: The users rating of restaurant

    :return: True or False
    """
    choices = [models.VisitHistory.HATE, models.VisitHistory.SAVE,
               models.VisitHistory.UNDECIDED]
    if rating.upper() not in choices:
        return False

    try:
        restaurant, created = models.VisitHistory.objects.get_or_create(
            user_id=user_id,
            search_id=search_id,
            restaurant_id=restaurant_id,
            rating=rating,
            last_visited=datetime.datetime.now())
    except db.IntegrityError as error:
        return False

    return created
