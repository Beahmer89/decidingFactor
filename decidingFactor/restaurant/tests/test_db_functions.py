from django.contrib.auth.models import User
from django.core import exceptions
from django.test import TestCase

from restaurant import db_functions
from restaurant.models import Location, SearchHistory, Restaurant
from restaurant.tests import helpers


class SearchFunctionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='Death', email='reaper@grim.com', password='Muerte666')
        self.location = Location.objects.create(city='Pittsburgh')
        self.portland = Location.objects.create(city='Portland')
        SearchHistory.objects.create(user_id=self.user,
                                     location_id=self.portland,
                                     search_terms="vegan pizza")

    def test_search_doesnt_already_exist(self):
        terms = "vegan"
        location = "Portland"

        resp = db_functions.check_if_search_exists(self.user, location, terms)
        self.assertIsNone(resp)

    def test_search_already_exists(self):
        terms = "vegan pizza"
        location = "Portland"

        resp = db_functions.check_if_search_exists(self.user, location, terms)
        self.assertIsNotNone(resp)

    def test_save_from_info_success(self):
        terms = "vegan"
        location = "Philadelphia"

        with self.assertRaises(exceptions.ObjectDoesNotExist):
            Location.objects.get(city=location)

        db_functions.save_search_form_info(self.user, location, terms)

        saved_loc = Location.objects.get(city=location)
        search_terms = SearchHistory.objects.get(user_id=self.user.pk,
                                                 location_id=saved_loc.pk)
        self.assertEquals(saved_loc.city, location)
        self.assertEquals(search_terms.search_terms, terms)

    def test_save_search_form_info_succeeds_with_existing_location(self):
        terms = "vegan pizza"
        location = "Pittsburgh"

        saved_loc = Location.objects.get(city=location)
        self.assertEquals(saved_loc.city, location)

        db_functions.save_search_form_info(self.user, location, terms)

        saved_loc = Location.objects.get(city=location)
        search_terms = SearchHistory.objects.get(user_id=self.user.pk,
                                                 location_id=saved_loc.pk)
        self.assertEquals(saved_loc.city, location)
        self.assertEquals(search_terms.search_terms, terms)


class VisitFunctionTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='Death', email='reaper@grim.com', password='Muerte666')
        self.user1 = User.objects.create_user(
            username='Nightman', email='nightman123@gmail.com',
            password='nightmancometh123')
        self.location = Location.objects.create(city='Philadelphia')
        self.portland = Location.objects.create(city='Portland')
        self.search = SearchHistory.objects.create(user_id=self.user,
                                                   location_id=self.portland,
                                                   search_terms="vegan")
        helpers.create_visit_history(self.location, self.search, self.user)

    def test_vist_history_returned_with_correct_data(self):
        history = db_functions.get_user_visit_history(self.user)

        self.assertEquals(len(history), len(helpers.RESTAURANTS))
        for restaurant in history:
            self.assertTrue(helpers.RESTAURANTS[restaurant['name']])

    def test_visit_history_returns_empty_for_user_with_no_history(self):
        history = db_functions.get_user_visit_history(self.user1)
        self.assertEquals(len(history), 0)


class RestaurantFunctionTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='Death', email='reaper@grim.com', password='Muerte666')
        self.location = Location.objects.create(city='Philadelphia')
        self.portland = Location.objects.create(city='Portland')
        self.search = SearchHistory.objects.create(user_id=self.user,
                                                   location_id=self.portland,
                                                   search_terms="vegan")

    def test_restaurant_saved(self):
        name = 'Pizza Brain'
        restaurant_type = 'pizza'
        price = '$'

        result = db_functions.save_restaurant_selection(name, self.location,
                                                        price, restaurant_type)
        self.assertIsNotNone(result)

        new_restaurant = Restaurant.objects.get(name=name)
        self.assertIsNotNone(new_restaurant)

    def test_db_integrity_error_is_caught_and_restaurant_not_saved(self):
        name = 'Bad'
        restaurant_type = 'french'
        price = '$$$'

        result = db_functions.save_restaurant_selection(name, None, price,
                                                        restaurant_type)

        self.assertIsNone(result)

        count = Restaurant.objects.filter(name=name).count()
        self.assertEquals(count, 0)

    def test_db_integrity_error_is_caught_and_visit_history_not_saved(self):
        name = 'Horrible'
        restaurant_type = 'soup'
        price = '$'

        result = db_functions.save_restaurant_selection(name, None, price,
                                                        restaurant_type)
        visit = db_functions.save_visit_selection(self.user, self.search,
                                                  None, 'undecided')

        self.assertFalse(visit)

        count = Restaurant.objects.filter(name=name).count()
        self.assertEquals(count, 0)

    def test_visit_history_saved(self):
        name = 'Lunas Paw Spot'
        restaurant_type = 'Chinese'
        price = '$$'

        result = db_functions.save_restaurant_selection(name, self.location,
                                                        price, restaurant_type)

        visit = db_functions.save_visit_selection(self.user, self.search,
                                                  result, 'undecided')

        self.assertTrue(visit)

        count = Restaurant.objects.filter(visithistory__user_id=self.user).count()
        self.assertEquals(count, 1)

    def test_visit_history_saved_not_saved_with_unknown_rating(self):
        name = 'Not Great'
        restaurant_type = 'Bulgarian'
        price = '$$'

        result = db_functions.save_restaurant_selection(name, self.location,
                                                        price, restaurant_type)

        visit = db_functions.save_visit_selection(self.user, self.search,
                                                  result, 'never again')

        self.assertFalse(visit)

        count = Restaurant.objects.filter(visithistory__user_id=self.user).count()
        self.assertEquals(count, 0)
