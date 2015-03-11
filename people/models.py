from django.conf import settings
from django.core.validators import ValidationError
from django.db import models, transaction

from csv import DictReader as csvrd
from datetime import datetime
import os, slugify, re

def validate_pic_extension(value):
	"""Checks if the picture format is '.jpg'"""
	if not value.name.endswith(".jpg"):
		raise ValidationError("Wrong Picture Format. Use .jpg")

class Person(models.Model):
	"""Holds all the information for one Person."""
	name = models.CharField(max_length=50)
	name_slug = models.SlugField(unique=True)
	classification = models.CharField(max_length=50, blank=True, help_text="Put faculty/staff/ga here as well as Fr/So/Jr/Sr")
	major = models.CharField(max_length=50, blank=True, help_text="Leave empty if not in a major.")
	society = models.CharField(max_length=50, blank=True, help_text="Put department here if faculty/staff")
	pic_url = models.CharField("Port_name", max_length=128, help_text="Put just the name of the image (no file path info).",\
					validators=[validate_pic_extension,])
	
	
	def __unicode__(self):
		return self.name

	class Meta():
		verbose_name_plural = "People"
		ordering = ['name']


def validate_file_extension(value):
	"""Checks if a file ends with '.csv'."""
	if not value.name.endswith('.csv'):
		raise ValidationError('Wrong file type. Use .csv file.')


class PeopleFile(models.Model):
	"""Expects a '.csv' file and attempst to create a Person object out of the rows, then creates an error log.
		Should be read-only after creation."""
	f = models.FileField("Upload File", upload_to='people', help_text='must be a .csv file with the following named columns:\
							name, major, society, classification, port_name', validators=[validate_file_extension,])
	result_f = models.CharField("Log", max_length=128, blank=True)
	successful = models.BooleanField("Status")
	num_errors = models.IntegerField()

	def __unicode__(self):
		return self.f.name

	def save(self, *args, **kwargs):
		# save to force django to upload the file
		self.num_errors = 0
		self.successful = True
		super(PeopleFile, self).save(*args, **kwargs)

		# create needed lists
		error_log = []
		classification_list = ['Freshman', 'Sophomore', 'Junior', 'Senior', 'Post-Graduate',\
							 'Graduate Assistant', 'Graduate Assistant', 'Faculty', 'Staff']
							 # yes, Graduate Assistant is supposed to be there twice!

		# read the file and attempt to create People objects out of the records
		with open(self.f.path, 'r') as csv_f:
			rd = csvrd(csv_f)
			for row in rd:
				try:
					# use atomic to reset the operations if an invalid create is attempted
					with transaction.atomic():
						final_name = ''
						
						# attempt to put the name in the proper format
						name_chunks = row['name'].strip().split()

						# if first name is one letter, leave it alone
						if not re.search('\w\.', name_chunks[0]):
							# check if last chunk is in this list
							if name_chunks[-1] in ['Jr.', 'Sr.', 'I', 'II', 'III', 'IV']:
								end = 2
							else:
								end = 1
							# abbreviate all the middle names.
							for i in range(1, len(name_chunks)-end):
								name_chunks[i] = name_chunks[i][0] + '.'
						
						# put the pieces back together
						final_name = ' '.join(name_chunks)

						# create a person in the database
						Person.objects.create(name=final_name.strip(), major=row['major'].strip(),\
									society=row['society'].strip(), pic_url=row['port_name'].strip(),\
									classification=classification_list[int(row['classification'])-1], \
									name_slug=slugify.slugify(final_name))

				except Exception as e:
					# count the errors
					self.num_errors += 1
					# put the error in the error log list with the name
					error_log.append(row['name'].strip()+': '+str(e)+'\n')

		# check if there were any errors
		if self.num_errors != 0:
			self.successful = False

		# create a log file with the timestamp as the name
		self.result_f = datetime.now().strftime("error_log_%Y%m%d_%H%M.txt")
		with open(os.path.join(settings.MEDIA_ROOT, "logs", self.result_f), 'w') as log_f:
			# record the number of errors
			log_f.write(str(self.num_errors)+" Errors\n")
			# write the errors to the log file
			for line in error_log:
				log_f.write(line)
		
		# save updated info
		super(PeopleFile, self).save(*args, **kwargs)
