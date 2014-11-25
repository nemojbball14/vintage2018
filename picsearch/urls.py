from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from picsearch.views import SearchView, ResultsView, PersonView , HomeView

urlpatterns = patterns('',
	#have to write the view to override the dispatch method for login
    # url(r'^$', TemplateView.as_view(template_name="picsearch/home.html"), name='home'),
    url(r'^$', HomeView.as_view(), name='home'),

    url(r'^people/$', SearchView.as_view(), name='search'),
    url(r'^results/$', ResultsView.as_view(), name='results'),
    url(r'^results/(?P<name_slug>[\w-]+)/$', PersonView.as_view(), name='person'),
)