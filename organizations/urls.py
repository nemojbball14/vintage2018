from django.conf.urls import patterns, url
from django.views.generic import ListView
from organizations.models import Organization, OrganizationType
from organizations.views import OrganizationView, OrganizationAllView, OrganizationSpecialView

urlpatterns = patterns('',
    url(r'^organizations/$', OrganizationAllView.as_view(), name='organizations'),
    url(r'^organizations/(?P<special_slug>[\w-]+)/$', OrganizationSpecialView.as_view()),
    url(r'^organizations/(?P<type_slug>[\w-]+)/(?P<name_slug>[\w-]+)/$', OrganizationView.as_view()),
)