from django.conf.urls import patterns, include, url

import views


urlpatterns = patterns('',
    url(r'^$', views.LoginView.as_view(), name='login'),
    url(r'^authenticate/$', views.AuthenticationView.as_view(), name='authenticate'),
)
