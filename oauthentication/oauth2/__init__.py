from django.core.exceptions import ImproperlyConfigured

import requests
import simplejson as json
import logging
logger = logging.getLogger(__name__)


class BaseClient(object):
    def __init__(self, access_token):
        self.access_token = access_token
        if self.access_token is None:
            raise ImproperlyConfigured('access_token cannot be None')
        return super(BaseClient, self).__init__()
        
    def get(self, endpoint, params={}):
        raise NotImplementedError()

    def post(self, endpoint, params={}):
        raise NotImplementedError()
    
    def put(self, endpoint, params={}):
        raise NotImplementedError()

    def delete(self, endpoint, params={}):
        raise NotImplementedError()

class Client(BaseClient):
    pass
