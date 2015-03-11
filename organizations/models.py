from django.db import models
from people.models import Person

import os


class OrganizationType(models.Model):
	"""The heading for a group of Organizations."""
	name = models.CharField(max_length=50, unique=True)
	slug = models.SlugField(unique=True)
	
	def __unicode__(self):
		return self.name

	class Meta:
		ordering = ['name']


class Organization(models.Model):
	"""A specific Organization with a type."""
	org_type = models.ForeignKey(OrganizationType, verbose_name="Organization Type")
	name = models.CharField(max_length=50)
	people = models.ManyToManyField(Person, verbose_name="Members", blank=True)
	slug = models.SlugField()
	
	def __unicode__(self):
		return self.name

	class Meta:
		# only one Organization of the same name per OrganiztionType
		unique_together = (('org_type','name'))
		ordering = ['name']


class OrganizationPicture(models.Model):
	"""A picture that belongs to an Organization."""
	org = models.ForeignKey(Organization, verbose_name="Organization")
	pic = models.ImageField("Image", upload_to=os.path.join('public', 'OrganizationPictures'))

	def __unicode__(self):
		return self.org.name+'-'+self.pic.name


class OrganizationSpecial(models.Model):
	"""An Organization that does not have a type. Also, has people that are not in the database"""
	name = models.CharField(max_length=50)
	people = models.TextField(help_text="List all the names separated by commas.")
	slug = models.SlugField()
	
	def __unicode__(self):
		return self.name

	class Meta:
		ordering = ['name']


class OrganizationSpecialPicture(models.Model):
	"""A picture that belongs to an OrganizationSpecial."""
	org = models.ForeignKey(OrganizationSpecial, verbose_name="Organization")
	pic = models.ImageField("Image", upload_to=os.path.join('public', 'OrganizationPictures'))

	def __unicode__(self):
		return self.org.name+'-'+self.pic.name
