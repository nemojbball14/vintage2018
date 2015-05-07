from django.views import generic
from django.shortcuts import render, get_object_or_404, render_to_response
#for login required views
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from articles.models import Article


class ArticleView(generic.TemplateView):
    template_name = 'articles/article.html'

    def get_context_data(self, **kwargs):
        context = super(ArticleView, self).get_context_data(**kwargs)
        article_slug = self.kwargs['article_slug']
        
        the_article = get_object_or_404(Article, article_slug=article_slug)

        # Split the contents on newlines so that the template can put in <p> tags
        # Also filter out the empty strings
        context['intro'] = filter(None, the_article.intro.split('\n'))
        context['paragraph'] = filter(None, the_article.paragraph.split('\n'))
        context['paragraph2'] = filter(None, the_article.paragraph2.split('\n'))

        context['article'] = the_article
        return context

    #Remove after development finished
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(OrganizationAllView, self).dispatch(*args, **kwargs)
