import re
import json
import datetime
import operator
import itertools
from functools import reduce

from django.db.models import Q
from django.conf import settings
from django.views import generic
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, render_to_response
#for login required views
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from people.models import Person
from people.forms import SearchForm
from organizations.models import Organization


def search_helper(query, major_exact_match, student_only):
    """Function for instant search results."""
    model_list = []
    
    # Convert the query from mascot to Greek if it matches.
    query = settings.ALIASES.get(query.lower(), query)
    
    query = query.strip()
    
    # Make sure the search has at least 3 letters and no invalid characters
    if re.search('[\w ]{3}', query):
        if not re.search('[^a-zA-Z .]', query): 
                
            # Find all the people or organizations that have info containing the string
            people = Person.objects.filter(first_name__icontains=query) | \
                     Person.objects.filter(last_name__icontains=query) | \
                     Person.objects.filter(society__icontains=query)
            organizations = Organization.objects.filter(name__icontains=query)
            
            # Filter based off of extra constraints
            if major_exact_match:
                people |= Person.objects.filter(major=query)
            else:
                people |= Person.objects.filter(major__icontains=query)
            if student_only:
                people = people.exclude(classification="Faculty/Staff")

            # Split the query to match the parts independently
            info_chunks = query.split()
            
            if len(info_chunks) == 1:
                # Get the people whose names match exactly
                people_first = Person.objects.filter(first_name__iexact=info_chunks[0])
                people_last = Person.objects.filter(last_name__iexact=info_chunks[0])
                
                # Add their groups
                for person in people_first:
                  organizations |= Organization.objects.filter(name=person.society) 
                
                for person in people_last:
                  organizations |= Organization.objects.filter(name=person.society)
                
                # Get the groups that have people that match the query
                organizations |= Organization.objects.filter(people__first_name=info_chunks[0])
                organizations |= Organization.objects.filter(people__last_name=info_chunks[0])
                    
            elif len(info_chunks) == 2:
                # Get the people where one name matches exactly and one matches partially
                people_first_to_last = Person.objects.filter(first_name__iexact=info_chunks[0], last_name__icontains=info_chunks[1])
                people_last_to_first = Person.objects.filter(last_name__iexact=info_chunks[0], first_name__icontains=info_chunks[1])
                
                # Add their groups
                for person in people_first_to_last:
                  organizations |= Organization.objects.filter(name=person.society) 
                
                for person in people_last_to_first:
                  organizations |= Organization.objects.filter(name=person.society)
                
                # Get the groups where people match the query
                organizations |= Organization.objects.filter(people__first_name__icontains=info_chunks[0], people__last_name__icontains=info_chunks[1])
            
            if len(info_chunks) > 1:
                # Create query pieces for matching for all pieces independently
                query_people_name = [Q(first_name__icontains=x) | Q(last_name__icontains=x) for x in info_chunks]
                query_society = [Q(society__icontains=x) for x in info_chunks]
                query_major = [Q(major__icontains=x) for x in info_chunks]
                query_org_name = [Q(name__icontains=x) for x in info_chunks]

                # Put 'and's for the pieces and 'or's for the types
                people |= Person.objects.filter(reduce(operator.and_, query_people_name)) | \
                          Person.objects.filter(reduce(operator.and_, query_society)) | \
                          Person.objects.filter(reduce(operator.and_, query_major))
                          
                organizations |= Organization.objects.filter(reduce(operator.and_, query_org_name))

            return ([people.distinct(), organizations.distinct()])
        else:
            return([])
    else:
        return([])


def instant_all_search(request):   
    req = {}
    if request.is_ajax():
        query = request.POST['query']
        
        # Call the search function
        model_list = search_helper(query, False, False)
        
        req['view_link'] = "people_search/?people_q=" + query
        req['people_count'] = "0"
        req['people'] = []
        req['organization'] = []

        # Format the json from the matched model objects
        if model_list:
            req['people_count'] = str(len(model_list[0]))

            for person in model_list[0][0:4]:
                person_dict = {
                              'thumbnail': person.pic_name.replace("placeholder", "placeholder.jpg"),
                              'first': person.first_name,
                              'last': person.last_name,
                              'classification': person.classification,
                              'major': person.major, 
                              'url': person.get_absolute_url()
                              }
                req['people'].append(person_dict)
                
            for org in model_list[1]:
                org_dict = {
                           'thumbnail': org.thumb_nail.url,
                           'name': org.name,
                           'description': org.paragraph[:87] + "...",
                           'url': org.get_absolute_url()}
                req['organization'].append(org_dict)
        
    else:
        req ['name'] = ""
    
    response = json.dumps(req)
    return HttpResponse(response, mimetype="application/json")


def people_search(request):
    template_name = 'people/results.html'
    
    if 'people_q' in request.GET:
        query = request.GET['people_q']
        
        if query == "":
            return render_to_response(template_name, {'SearchForm':SearchForm(), 'query':query, 'timenow':datetime.datetime.now()}, RequestContext(request))
        
        # Determine if there are extra constraints
        if 'major_exact' in request.GET and request.GET['major_exact'] == "1":
            major_exact_match = True
        else:
            major_exact_match = False
        
        if 'student' in request.GET and request.GET['student'] == "1":
            student_only = True
        else:
            student_only = False
        
        # Call the search function
        model_list = search_helper(query, major_exact_match, student_only)
        
        if(len(model_list) == 0):
            length = 0
            return render_to_response("people/search.html", {'SearchForm':SearchForm(), 'query':query, 'message':"Invalid search.",
                                      'timenow':datetime.datetime.now()}, RequestContext(request))
        else:
            length = str(len(model_list[0]))
            return render_to_response(template_name, {'SearchForm':SearchForm(), 'query':query, 'people_list':model_list[0], 'resultLength':length ,
                                      'timenow':datetime.datetime.now()}, RequestContext(request))
    else:
        return render_to_response(template_name, {'SearchForm':SearchForm()})


class SearchView(generic.TemplateView):
    """View for the initial search page. Redirects to the results page if the query is valid."""
    template_name = 'people/search.html'

    def post(self, request, *args, **kwargs):
        info = self.request.POST.get('info','').strip()
        context = self.get_context_data(**kwargs)

        # Check the search string for at least 3 consecutive letters
        if re.search('[\w ]{3}', info):
            # Black listing invalid characters
            if not re.search('[^a-zA-Z .]', info):
                return HttpResponseRedirect(reverse('results')+'?info='+info)
            else:
                context['message'] = 'Invalid search. Please use only letters, spaces, and periods.'
        else:
            context['message'] = 'Invalid search. Please use at least 3 consecutive letters.'
        
        return render(request, self.template_name, context)
        
    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        
        context['SearchForm'] = SearchForm()
        
        return context

    #Remove after development finished
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SearchView, self).dispatch(*args, **kwargs)


class PersonView(generic.TemplateView):
    """Uses the results page to show one person. Redirects to 404 if invalid name slug is used."""
    template_name = 'people/results.html'

    def get_context_data(self, **kwargs):
        context = super(PersonView, self).get_context_data(**kwargs)
        name_slug = self.kwargs['name_slug']
        
        the_person = get_object_or_404(Person, name_slug=name_slug)
        context['people_list'] = [the_person,]
        context['SearchForm'] = SearchForm()
        return context

    #Remove after development finished
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SearchView, self).dispatch(*args, **kwargs)
