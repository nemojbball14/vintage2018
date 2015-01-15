from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from people.views import SearchView, ResultsView, PersonView

urlpatterns = patterns('',
    url(r'^people/$', SearchView.as_view(), name='search'),
    url(r'^results/$', ResultsView.as_view(), name='results'),
    url(r'^results/(?P<name_slug>[\w-]+)/$', PersonView.as_view(), name='person'),
)