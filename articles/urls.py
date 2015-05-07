from django.conf.urls import patterns, url
from articles.views import ArticleView

urlpatterns = patterns('',
    url(r'^articles/(?P<article_slug>[\w\d-]+)/$', ArticleView.as_view(), name='article'),
)
