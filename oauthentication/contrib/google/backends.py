from django.conf import settings
from django.contrib.auth.models import User, check_password

from oauthentication.backends.oauth2 import AuthenticationBackend as BaseOAuth2AuthenticationBackend
import requests
import simplejson as json
import logging
logger = logging.getLogger(__name__)


class OAuth2AuthenticationBackend(BaseOAuth2AuthenticationBackend):
    supports_inactive_user = False
    oauth2_userinfo_endpoint = 'https://www.googleapis.com/oauth2/v1/userinfo'

    def get_userinfo(self, access_token=None):
        response = requests.get(self.get_endpoint(), headers={
            'Authorization': 'Bearer {access_token}'.format(access_token=access_token)
        })
        
        if response.status_code != requests.codes.ok:
            logger.info(response.text)
            return None
            
        logger.info(json.loads(response.text))
        return json.loads(response.text)
