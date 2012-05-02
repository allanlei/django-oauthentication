from django.conf.urls import patterns, include, url
from django.views import generic
from django.core.urlresolvers import reverse_lazy as reverse
from django.conf import settings

from django.contrib.auth.decorators import login_required

#from oauthentication.contrib import googleapps

openid_patterns = patterns('',
#    url(r'^googleapps/', include(patterns('',
#        url(r'^$', generic.base.TemplateView.as_view(template_name='login.html'), name='login'),
#        url(r'^authenticate/$', generic.base.TemplateView.as_view(template_name='login.html'), name='authenticate'),
#    ), namespace='googleapps')),
)

oauth2_patterns = patterns('',
#    url(r'^googleapps/', include(patterns('',
#        url(r'^$', googleapps.views.LoginView.as_view(
##            template_name='registration/djauth/oauth2/googleapps/login.html',
#            authentication_callback_url=settings.OAUTH2_GOOGLEAPPS_REDIRECT_URI,
#            oauth2_client_id=settings.OAUTH2_GOOGLEAPPS_CLIENT_ID,
#        ), name='login'),
#        url(r'^authenticate/$', googleapps.views.AuthenticationView.as_view(
#            failure_url=reverse('accounts:login'),
#            oauth2_redirect_uri=settings.OAUTH2_GOOGLEAPPS_REDIRECT_URI,
#            oauth2_client_id=settings.OAUTH2_GOOGLEAPPS_CLIENT_ID,
#            oauth2_client_secret=settings.OAUTH2_GOOGLEAPPS_CLIENT_SECRET,
#        ), name='authenticate'),
#    ), namespace='googleapps')),
)

urlpatterns = patterns('',
    url(r'^$', generic.base.RedirectView.as_view(
        url=reverse('home'),
    )),
    
    url(r'^accounts/', include(patterns('',
        url(r'^login/$', generic.base.TemplateView.as_view(template_name='login.html'), name='login'),
#        url(r'^login/openid/', include(openid_patterns, namespace='openid')),
        url(r'^login/oauth2/', include(oauth2_patterns, namespace='oauth2')),
        
        url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
    ), namespace='accounts')),

    url(r'^accounts/profile/$', login_required(generic.base.TemplateView.as_view(template_name='index.html')), name='home'),
)
