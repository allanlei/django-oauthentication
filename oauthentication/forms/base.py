from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _

import logging
logger = logging.getLogger(__name__)


class LoginForm(forms.Form):
    pass


class AuthenticationForm(forms.Form):
    error_messages = {
        'invalid_login': _('Please enter a correct username and password. Note that both fields are case-sensitive.'),
        'inactive': _('This account is inactive.'),
    }

    def __init__(self, *args, **kwargs):
        self.user_cache = None
        self.credentials_cache = None
        super(AuthenticationForm, self).__init__(*args, **kwargs)
    
    def authenticate(self):
        '''
        Should return an authenticated User via authenticate(), credentials should be retrieved from self.cleaned_data
        '''
        raise NotImplementedError

    def clean(self):
        cleaned_data = super(AuthenticationForm, self).clean()
        self.user_cache = self.authenticate()
        
        if self.user_cache is None:
            raise forms.ValidationError(self.error_messages['invalid_login'])
        elif not self.user_cache.is_active:
            raise forms.ValidationError(self.error_messages['inactive'])
        return cleaned_data

    def get_user(self):
        return self.user_cache

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None
