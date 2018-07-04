from django.contrib.auth.models import User
from django.core import exceptions
from django.test import TestCase

from restaurant import db_functions
from restaurant.models import Location, SearchHistory


# Create your tests here.
class DatabaseFunctionTests(TestCase):
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

        db_functions.save_form_info(self.user, location, terms)

        saved_loc = Location.objects.get(city=location)
        search_terms = SearchHistory.objects.get(user_id=self.user.pk,
                                                 location_id=saved_loc.pk)
        self.assertEquals(saved_loc.city, location)
        self.assertEquals(search_terms.search_terms, terms)

    def test_save_form_info_succeeds_with_location_already_existing(self):
        terms = "vegan pizza"
        location = "Pittsburgh"

        saved_loc = Location.objects.get(city=location)
        self.assertEquals(saved_loc.city, location)

        db_functions.save_form_info(self.user, location, terms)

        saved_loc = Location.objects.get(city=location)
        search_terms = SearchHistory.objects.get(user_id=self.user.pk,
                                                 location_id=saved_loc.pk)
        self.assertEquals(saved_loc.city, location)
        self.assertEquals(search_terms.search_terms, terms)
