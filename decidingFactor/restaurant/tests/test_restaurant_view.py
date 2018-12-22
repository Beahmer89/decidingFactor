from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory

from restaurant import views
from restaurant.models import Location, SearchHistory
from restaurant.tests import helpers


class RestaurantTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='Death', email='reaper@grim.com', password='Muerte666')
        self.terms = 'vegan'
        self.portland = Location.objects.create(city='Portland')
        self.search = SearchHistory.objects.create(user_id=self.user,
                                                   location_id=self.portland,
                                                   search_terms=self.terms)
        helpers.new_create_visit_history(self.portland, self.terms,
                                         self.search, self.user)

    def test_success(self):
        request = self.factory.post('/restaurant/',
                                    {'name': 'Death', 'terms': 'vegan',
                                     'city': self.portland})
        request.user = self.user
        response = views.restaurant(request)
        self.assertEquals(response.status_code, 200)
