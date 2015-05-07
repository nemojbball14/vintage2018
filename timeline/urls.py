from django.conf.urls import patterns, url
from timeline.views import HomeView, WideSearchView

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^search/$', WideSearchView.as_view(), name='wide_search'),
)
