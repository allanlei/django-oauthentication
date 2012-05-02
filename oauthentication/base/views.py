from django.views import generic
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.sites.models import get_current_site
from django.contrib.auth import login

from oauthentication.exceptions import ResponseNotAuthenticException

import urlparse
import logging
logger = logging.getLogger(__name__)



class LoginView(generic.edit.FormView):    
    authentication_url = None
    authentication_callback_url = None

    def get_form_class(self):
        form_class = super(LoginView, self).get_form_class()
        if not form_class:
            raise ImproperlyConfigured('LoginView must be paired with an instance of djauth.forms.LoginForm')
        return form_class
    
    def get_authentication_callback_url(self):
        url = self.authentication_callback_url
        if url:
            return str(url)
        return None
        
    def get_authentication_url(self):
        return self.authentication_url
    
    def get_success_url(self):
        return self.get_authentication_url()





'''
    Following django's django.contrib.auth.views.login
    1. Response should be authenticated inside the AuthenticationForm.  Need to customize where the data comes from since OAuth 2.0 uses redirects and therefore HTTP GET requests instead of reading from POST.
    2. Instead of copy and pasting django.contrib.auth.views.login, just call it as login(self.request, authentication_form=AuthenticationForm)
        Signature:  login(request, template_name='registration/login.html', redirect_field_name=REDIRECT_FIELD_NAME, authentication_form=AuthenticationForm, current_app=None, extra_context=None)
'''  
class AuthenticationView(generic.edit.FormView):
#    http_method_names = ['get']     #Use this option to whitelist what methods get through
    http_authentication_methods = ['get', 'post']
    redirect_field_name = REDIRECT_FIELD_NAME
    failure_url = None

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def get_redirect_field_name(self):
        if self.redirect_field_name:
            field = self.redirect_field_name
        else:
            field = ''
        return field

    def get_form_class(self):
        form_class = super(AuthenticationView, self).get_form_class()
        if not form_class:
            raise ImproperlyConfigured('AuthenticationView must be paired with an instance of djauth.forms.AuthenticationForm')
        return form_class

    def get_form_kwargs(self):
        kwargs = super(AuthenticationView, self).get_form_kwargs()
        kwargs.update({
            'data': self.get_authentication_data(),
        })
        return kwargs

    def get_authentication_data(self):
        data = getattr(self.request, self.request.method.upper(), None)
        return data.dict() if data else None
        
    def form_valid(self, form):
        logger.info('VALID')
        login(self.request, form.get_user())
        logger.info(self.request.user.backend)
        
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()
        return super(AuthenticationView, self).form_valid(form)

    def get_success_url(self):
        redirect_to = self.request.REQUEST.get(self.get_redirect_field_name(), '')
        netloc = urlparse.urlparse(redirect_to)[1]
        if not redirect_to:
            redirect_to = settings.LOGIN_REDIRECT_URL
        elif netloc and netloc != self.request.get_host():
            redirect_to = settingWs.LOGIN_REDIRECT_URL
        return redirect_to

    def get_failure_url(self):
        if self.failure_url:
            url = self.failure_url
        else:
            url = None
        return url

    def form_invalid(self, form):
        for field, error in form.errors.items():
            logger.info(field)
            logger.info(error)

        redirect_to = self.get_failure_url()
        if redirect_to:
            return HttpResponseRedirect(redirect_to)
        return super(AuthenticationView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(AuthenticationView, self).get_context_data(**kwargs)
        
        current_site = get_current_site(self.request)
        context.update({
            'site': current_site,
            'site_name': current_site.name,
            self.get_redirect_field_name(): self.get_success_url(),
        })
        return context
        
    def render_to_response(self, context, **kwargs):
        self.request.session.set_test_cookie()
        return super(AuthenticationView, self).render_to_response(context, **kwargs)
