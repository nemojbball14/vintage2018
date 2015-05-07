from django.views import generic
#for login required views
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from people.forms import SearchForm
from articles.models import Article


class WideSearchView(generic.TemplateView):
    template_name = 'timeline/search.html'

    def get_context_data(self, **kwargs):
        context = super(WideSearchView, self).get_context_data(**kwargs)
        
        context['SearchForm'] = SearchForm()
        
        return context

    #Remove after development finished
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(HomeView, self).dispatch(*args, **kwargs)


class HomeView(generic.TemplateView):
    template_name = 'timeline/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        all_articles = Article.objects.all()
        context['article_dict'] = { a.article_slug : a for a in all_articles }
        context['intro_dict'] = { a.article_slug : filter(None, a.intro.split('\n')) for a in all_articles }

        return context

    #Remove after development finished
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(HomeView, self).dispatch(*args, **kwargs)
