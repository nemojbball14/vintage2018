from django.conf.urls import patterns, url
from django.views.generic import ListView
from timeline.views import HomeView

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='home'),
)