from django.views import generic
from django.shortcuts import render, get_object_or_404
#for login required views
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from organizations.models import Organization, OrganizationType, OrganizationPicture, OrganizationSpecial
from people.models import Person


class OrganizationAllView(generic.TemplateView):
	"""Retrieves all the Organizations under every OrganizationType and the special ones."""
	template_name = 'organizations/organization_all.html'
	
	def get_context_data(self, **kwargs):
		context = super(OrganizationAllView, self).get_context_data(**kwargs)
		the_types = list(OrganizationType.objects.all()) + \
					list(OrganizationSpecial.objects.all())

		the_types = sorted(the_types, key=lambda x: x.name)
		
		all_orgs = []
		for t in the_types:
			orgs = Organization.objects.filter(org_type=t)
			all_orgs.append((t, orgs))
		
		context['org_list'] = all_orgs
		return context

	#Remove after development finished
	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(OrganizationAllView, self).dispatch(*args, **kwargs)


class OrganizationView(generic.TemplateView):
	"""Shows a specific Organization based off the url or displays a 404."""
	template_name = 'organizations/organization.html'
	
	def get_context_data(self, **kwargs):
		context = super(OrganizationView, self).get_context_data(**kwargs)
		the_type = get_object_or_404(OrganizationType, slug=self.kwargs['type_slug'])
	
		context['org'] = get_object_or_404(Organization, slug=self.kwargs['name_slug'], org_type=the_type)

		# if the organization is a society, pull the people automatically
		if the_type.slug in ("mens-societies","womens-societies"):
			context['people'] = Person.objects.filter(society=context['org'])

		return context

	#Remove after development finished
	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(OrganizationView, self).dispatch(*args, **kwargs)


class OrganizationSpecialView(generic.TemplateView):
	"""Shows a special Organization based off the url or displays a 404."""
	template_name = 'organizations/organization_special.html'
	
	def get_context_data(self, **kwargs):
		context = super(OrganizationSpecialView, self).get_context_data(**kwargs)	
		context['org'] = get_object_or_404(OrganizationSpecial, slug=self.kwargs['special_slug'])

		# split the list of people by commas
		temp = context['org'].people.split(',')
		# then sort the list
		temp.sort()
		context['members'] = temp

		return context

	#Remove after development finished
	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(OrganizationSpecialView, self).dispatch(*args, **kwargs)