from oauthentication.views.oauth2 import LoginView, AuthenticationView

from forms import LoginForm, AuthenticationForm

import logging
logger = logging.getLogger(__name__)


'''
https://code.google.com/apis/console/ to manage OAuth 2.0 codes
'''
    
class LoginView(LoginView):
    form_class = LoginForm
    oauth2_authorization_endpoint = 'https://accounts.google.com/o/oauth2/auth'
    oauth2_google_access_type = None
    oauth2_google_approval_prompt = None
    
    def get_oauth2_scopes(self):
        return [
            'https://www.googleapis.com/auth/userinfo.profile', 
            'https://www.googleapis.com/auth/userinfo.email',
        ]

    def get_oauth2_google_access_type(self):
        if self.oauth2_google_access_type:
            access_type = self.oauth2_google_access_type
        else:
            access_type = None
        return access_type
        
    def get_oauth2_google_approval_prompt(self):
        if self.oauth2_google_approval_prompt:
            prompt = self.oauth2_google_approval_prompt
        else:
            prompt = None
        return prompt
        
    def get_oauth2_authorization_parameters(self):
        parameters = super(LoginView, self).get_oauth2_authorization_parameters()
        
        access_type = self.get_oauth2_google_access_type()
        if access_type:
            parameters['access_type'] = access_type

        approval_prompt = self.get_oauth2_google_approval_prompt()
        if approval_prompt:
            parameters['approval_prompt'] = approval_prompt
        return parameters
    
class AuthenticationView(AuthenticationView):
    form_class = AuthenticationForm
    oauth2_access_endpoint = 'https://accounts.google.com/o/oauth2/token'
