from functools import reduce
from django.db.models import Q
from django.views import generic
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
#for login required views
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

import re, operator

from django.conf import settings
from people.models import Person


class SearchView(generic.TemplateView):
	"""View for the initial search page. Redirects to the results page if the query is valid."""
	template_name = 'people/search.html'

	def post(self, request, *args, **kwargs):
		info = self.request.POST.get('info','').strip()
		context = self.get_context_data(**kwargs)

		#check the search string for at least 3 consecutive letters
		if re.search('[\w ]{3}', info):
			if not re.search('[^a-zA-Z .]', info):
				return HttpResponseRedirect(reverse('results')+'?info='+info)
			else:
				context['message'] = 'Invalid search. Please use only letters, spaces, and periods.'
		else:
			context['message'] = 'Invalid search. Please use at least 3 consecutive letters.'
		
		return render(request, self.template_name, context)

	#Remove after development finished
	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(SearchView, self).dispatch(*args, **kwargs)
		

class ResultsView(generic.TemplateView):
	"""Shows the results for the current query."""
	template_name = 'people/results.html'
	
	def post(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		return render(request, self.template_name, context)
	
	def get_context_data(self, **kwargs):
		context = super(ResultsView, self).get_context_data(**kwargs)

		info = self.request.GET.get('info','').strip()

		context['search_info'] = info

		#Change society mascot names to their Greek
		info = settings.ALIASES.get(info.lower(), info)
		
		#check the search string for at least 3 consecutive letters
		if re.search('[\w ]{3}', info):
			if not re.search('[^a-zA-Z .]', info): 
				
				#find all the people that have info containing the string
				people = Person.objects.filter(name__icontains=info) | \
					     Person.objects.filter(society__icontains=info) | \
					     Person.objects.filter(major__icontains=info)

				#if there are at least two pieces, split them apart and look for all independently
				info_chunks = info.split()
				if len(info_chunks) > 1:
					query1 = [Q(name__icontains=x) for x in info_chunks]
					query2 = [Q(society__icontains=x) for x in info_chunks]
					query3 = [Q(major__icontains=x) for x in info_chunks]

					people |= Person.objects.filter(reduce(operator.and_, query1)) | \
							  Person.objects.filter(reduce(operator.and_, query2)) | \
							  Person.objects.filter(reduce(operator.and_, query3))

				count = len(people)

				context['people_list'] = people

				if count != 1:
					context['message'] = '{} results found for \"{}.\"'.format(count, info)
				else:
					context['message'] = '1 result found for \"{}.\"'.format(info)

			else:
				context['message'] = 'Invalid search. Please use only letters, spaces, and periods.'
		else:
			context['message'] = 'Invalid search. Please use at least 3 consecutive letters.'
		return context

	#Remove after development finished
	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(ResultsView, self).dispatch(*args, **kwargs)


class PersonView(generic.TemplateView):
	"""Uses the results page to show one person. Redirects to 404 if invalid name slug is used."""
	template_name = 'people/results.html'

	def get_context_data(self, **kwargs):
		context = super(PersonView, self).get_context_data(**kwargs)
		name_slug = self.kwargs['name_slug']
		
		the_person = get_object_or_404(Person, name_slug=name_slug)
		context['people_list'] = [the_person,]
		return context
		
	#Remove after development finished
	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(PersonView, self).dispatch(*args, **kwargs)
