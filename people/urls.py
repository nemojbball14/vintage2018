from django.conf.urls import patterns, url
from people.views import SearchView, PersonView

urlpatterns = patterns('',
    url(r'^people/$', SearchView.as_view(), name='search'),
    url(r'^results/(?P<name_slug>[\w-]+)/$', PersonView.as_view(), name='person'),
    url(r'^instant_all_search$', 'people.views.instant_all_search'),
    url(r'^people_search/$', 'people.views.people_search'),
)
