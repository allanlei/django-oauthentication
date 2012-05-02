from django import forms
from oauthentication.forms import oauth2

import requests
import simplejson as json
import logging
logger = logging.getLogger(__name__)


class LoginForm(oauth2.LoginForm):
    domain = forms.RegexField('^[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.(([a-zA-Z]{2,3})|(aero|coop|info|museum|name))$', max_length=253)

class AuthenticationForm(oauth2.AuthenticationForm):
    oauth2_token_endpoint = 'https://accounts.google.com/o/oauth2/token'
