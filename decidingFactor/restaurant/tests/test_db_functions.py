from django.contrib.auth.models import User
from django.core import exceptions
from django.test import TestCase

from restaurant import db_functions
from restaurant.models import Location, SearchHistory
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
