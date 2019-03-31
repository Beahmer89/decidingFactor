from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory

from restaurant import views
from restaurant.models import Location, SearchHistory
from restaurant.tests import helpers


class RestaurantTests(TestCase):
    fixtures = ['new.yaml']

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.get(username='test')
        self.terms = 'vegan'

    def test_success(self):
        request = self.factory.post('/restaurant/',
                                    {'name': 'Death', 'terms': 'vegan',
                                     'city': 'portland'})
        request.user = self.user
        response = views.restaurant(request)
        self.assertEquals(response.status_code, 200)
