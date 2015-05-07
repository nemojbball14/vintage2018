import os
import re
import slugify

from django.conf import settings
from django.db import models, transaction
from django.core.urlresolvers import reverse
from django.core.validators import ValidationError

from csv import DictReader
from datetime import datetime


def validate_pic_extension(value):
    """Checks if the picture format is '.jpg'"""
    if not (value.endswith(".jpg") or value == "placeholder"):
        raise ValidationError("Wrong Picture Format. Use .jpg")


class Person(models.Model):
    """Holds all the information for one Person."""
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50 , blank=True)
    surtitle = models.CharField(max_length=50, blank=True)
    
    name_slug = models.SlugField(unique=True)
    classification = models.CharField(max_length=50, blank=True, help_text="Put faculty/staff/ga here as well as Fr/So/Jr/Sr")
    major = models.CharField(max_length=50, blank=True, help_text="Leave empty if not in a major.")
    society = models.CharField(max_length=50, blank=True, help_text="Put department here if faculty/staff")
    pic_name = models.CharField("Portrait Name", max_length=128, help_text="Put just the name of the image (no file path info).",\
                                validators=[validate_pic_extension,])
    thumb_nail = models.CharField(max_length=128, help_text="Put just the name of the image (no file path info).",\
                                validators=[validate_pic_extension,])
    
    def __unicode__(self):
        return "{} {} {}, {}".format(self.first_name, self.middle_name, self.last_name, self.major)
    
    def __str__(self):
        return self.first_name + " " +  self.last_name
    
    def get_absolute_url(self):
        return reverse("person", args=[self.name_slug])
        
    class Meta():
        verbose_name_plural = "People"
        ordering = ['last_name', 'first_name']


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
        # save to force django to actually upload the file
        self.num_errors = 0
        self.successful = True
        super(PeopleFile, self).save(*args, **kwargs)

        # Read the file and attempt to create People objects out of the records
        error_log = []
        # cls = ['Freshman', 'Sophomore', 'Junior', 'Senior', 'Post-Graduate', 'Graduate Student', \
        #       'Graduate Student', 'Faculty', 'Staff']
                #yes, Graduate Student is supposed to be there twice!

        with open(self.f.path, 'r') as csv_input_file:
            dict_reader = DictReader(csv_input_file)
            for row in dict_reader:
                try:
                    # Use atomic to reset the operations if an invalid create is attempted
                    with transaction.atomic():

                        # Creates a person based off of gathered information.
                        if row['port_name'].endswith(".jpg"):
                            thumb_nail = row['port_name'][:-4] + "_thumb.jpg"
                        else:
                            thumb_nail = "placeholder"

                        Person.objects.create(first_name=row["first_name"].strip(),
                            middle_name=row["middle_name"].strip(),
                            last_name=row["last_name"].strip(),
                            surtitle=row["surtitle"].strip(),
                            major=row['major'].strip(),
                            society=row['society'].strip(),
                            pic_name=row['port_name'],
                            thumb_nail=thumb_nail,
                            classification=row['classification'],
                            name_slug=slugify.slugify(" ".join([ row["first_name"], row["last_name"]])))
                except Exception as e:
                    # Store the errors
                    # Note: if you get "Some non-transactional changed tables couldn't be rolled back," you need to change the database engine
                    self.num_errors += 1
                    error_log.append("{} {}: {}\n".format(row['first_name'], row['last_name'], e))

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
