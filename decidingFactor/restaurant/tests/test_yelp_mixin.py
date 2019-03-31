import json
import mock
import os
import requests

from restaurant.mixins.yelp import YelpClient

from django.test import TestCase
from django.test import SimpleTestCase

class YelpTests(TestCase):

    def setUp(self):
        self.yelp = YelpClient(os.getenv('YELP_API_KEY'))

    def test_find_businesses_returns_success(self):
        results = self.yelp.find_businesses(location="Portland", term="vegan")
        restaurants = json.loads(results.content.decode('utf-8'))

        self.assertIsNotNone(restaurants.get('businesses'))

    def test_find_businesses_returns_success_with_utf8_chars(self):
        results = self.yelp.find_businesses(location="Tokyo", term="たこ焼き")
        restaurants = json.loads(results.content.decode('utf-8'))

        self.assertIsNotNone(restaurants.get('businesses'))

    def test_wrong_api_key_results_in_400(self):
        yelp_fail = YelpClient("fake_api_key")

        results = yelp_fail.find_businesses(location="Minnesota", term="tacos")
        self.assertEquals(results.status_code, 400)

    def test_retrys_occur_on_423_level_error(self):
        with mock.patch('restaurant.mixins.yelp.YelpClient.SLEEP_DURATION',
                        new_callable=mock.PropertyMock) as t:
            t.return_value = .01
            with mock.patch('requests.request') as request:
                response = mock.Mock(status_code=423)
                request.return_value = response
                results = self.yelp.find_businesses(location="Tampa",
                                                    term="subs")

        self.assertEquals(request.call_count, 3)

    def test_wrong_host_results_in_599(self):
        yelp_fail = YelpClient(os.getenv('YELP_API_KEY'), "api.yelp.com.blah")
        results = yelp_fail.find_businesses(location="California",
                                            term="sushi")

        self.assertEquals(results.status_code, 599)

    def test_retrys_occur_on_500_level_error(self):
        with mock.patch('requests.request') as request:
            response = mock.Mock(status_code=500)
            request.return_value = response

            results = self.yelp.find_businesses(location="Tokyo", term="vegan")

        self.assertEquals(request.call_count, 3)
