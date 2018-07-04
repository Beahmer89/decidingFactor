import logging
import requests
import time
from urllib import parse

from django import http

API_VERSION = 'v3'
AUTH_HEADER = 'bearer {}'
DEFAULT_HOST = 'api.yelp.com'
SCHEMA = 'https'

LOGGER = logging.getLogger(__name__)


class YelpClient(object):

    HTTP_RETRIES = 3
    SLEEP_DURATION = 3
    TIMEOUT = 20

    def __init__(self, cert=None, host=DEFAULT_HOST):
        self.cert = cert
        self.host = host
        self.base_url = self._build_url()

    def find_businesses(self, location, term=None, latitude=None,
                        longitude=None, radius=None, categories=None,
                        locale=None, limit=None, offset=None,
                        sort_by='best_match', price=None, open_now=False,
                        open_at=None, attributes=None):
        query_params = {key: val for key, val in locals().items()
                        if key != 'self' and val}
        endpoint = 'businesses/search'
        url = self.base_url + endpoint
        return self._http_request(url, query_params)

    def _build_url(self):
        """ Setup the request needed to be made for YELP to get information"""
        return '{0}://{1}/{2}/'.format(SCHEMA,
                                       parse.quote(self.host, ''),
                                       API_VERSION)

    def _http_request(self, url, query_params=None,
                      body={}, request_type='GET'):
        """This function is meant to be a generic in order to execute different
        types of HTTP requests. For now in this project, we only need a GET in
        order to get information from YELP. Include type param if other
        requests are needed.

        """
        auth_header = AUTH_HEADER.format(self.cert)
        headers = {'Authorization': auth_header,
                   'Content-Type': 'application/json'}

        response = None
        for x in range(0, self.HTTP_RETRIES):
            try:
                response = requests.request(request_type, url,
                                            params=query_params,
                                            headers=headers, data=body,
                                            timeout=self.TIMEOUT)
            except requests.exceptions.RequestException as error:
                LOGGER.error('An error occurred when trying to make request to'
                             ' {}. Error: {}'.format(url, error))
                continue

            if 200 <= response.status_code < 400:
                return http.HttpResponse(status=response.status_code,
                                         reason=response.reason,
                                         content=response,
                                         content_type='application/json')
            elif response.status_code in [423, 429]:
                LOGGER.warning('Yelp Rate limited retrying in {} '
                               ' seconds'.format(self.SLEEP_DURATION))
                time.sleep(self.SLEEP_DURATION)
            elif 400 <= response.status_code < 500:
                LOGGER.error('Yelp 400 lvl error: {}'.format(response.reason))
                return http.HttpResponse(status=response.status_code,
                                         reason=response.reason)
            elif response.status_code >= 500:
                LOGGER.error('Yelp 500 lvl error: {}'.format(response.reason))

        if response:
            return http.HttpResponse(status=response.status_code,
                                     reason=response.reason,
                                     content=response,
                                     content_type='application/json')
        else:
            return http.HttpResponse(status=599,
                                     reason="Network Connection Timeout Error")
