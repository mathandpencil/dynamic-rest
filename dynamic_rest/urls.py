"""
Login and logout views for the admin API.

Add these to your root URLconf if you're using the browsable API and
your API requires authentication:

    urlpatterns = [
        ...
        url(r'^auth/', include('rest_framework.urls', namespace='rest_framework'))
    ]

In Django versions older than 1.9, the urls must be namespaced as 'rest_framework',
and you should make sure your authentication settings include `SessionAuthentication`.
"""  # noqa
from __future__ import unicode_literals

from django.conf.urls import url
from django.contrib.auth import views
from dynamic_rest.conf import settings as drest

template_name = {'template_name': drest.LOGIN_TEMPLATE}

app_name = 'dynamic_rest'
urlpatterns = [
    url(r'^login/$', views.login, template_name, name='login'),
    url(r'^logout/$', views.logout, template_name, name='logout'),
]
