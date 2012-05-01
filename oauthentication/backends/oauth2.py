from django.conf import settings
from django.contrib.auth.models import User

from oauthentication.backends import AuthenticationBackend as BaseAuthenticationBackend
import requests
import simplejson as json
import logging
logger = logging.getLogger(__name__)


class AuthenticationBackend(BaseAuthenticationBackend):
    supports_inactive_user = False
    create_unknown_user = False
    oauth2_userinfo_endpoint = None     #Endpoint for info
    credentials_fields = ['email']
    
    def authenticate(self, access_token=None):
        if access_token is None:
            return None
        return super(AuthenticationBackend, self).authenticate(access_token=access_token)
    
    def get_credentials(self, access_token=None):
        userinfo = self.get_userinfo(access_token=access_token)
        
        if not userinfo:
            return None
        return super(AuthenticationBackend, self).get_credentials(userinfo)

    def get_endpoint(self):
        if self.oauth2_userinfo_endpoint:
            endpoint = self.oauth2_userinfo_endpoint
        else:
            raise ImproperlyConfigured('Provide the OAuth 2.0 userinfo endpoint')
        return endpoint
    
    def get_endpoint_params(self):
        return {}

    def get_userinfo(self, access_token=None):
        params = self.get_endpoint_params()
        params.update({
            'access_token': access_token,
        })
        
        logger.info(self.get_endpoint())
        logger.info(params)
        response = requests.get(self.get_endpoint(), data=params)
        
        if response.status_code != requests.codes.ok:
            logger.info(response.text)
            return None
            
        logger.info(json.loads(response.text))
        return json.loads(response.text)
