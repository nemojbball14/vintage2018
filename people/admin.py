from django.contrib import admin
from people.models import Person, PeopleFile


def TypoFixer(modeladmin, request, queryset):
	"""Use this function to mass edit a typo. Just be sure to only apply it to the correct people!
		Change the value inside 'update' to whatever needs to be changed.
		Uncomment the 'action' line below in PersonAdmin to enable. (I also recommend you disable it
		after the typo is fixed.)"""
	queryset.update(classification="Sophomore")


class PersonAdmin(admin.ModelAdmin):
	prepopulated_fields = {"name_slug": ("name",)} 
	list_display = ('name', 'classification', 'major', 'society', 'pic_url')
	fields = ('name', 'name_slug','classification', 'major', 'society', 'pic_url',)
	list_filter = ['classification', 'major', 'society']
	ordering = ('name',)
	# actions = [TypoFixer,]


class PeopleFileAdmin(admin.ModelAdmin):
	list_display = ('f', 'successful', 'result_f')
	fields = ('f',)
	actions = None

	def get_readonly_fields(self, request, obj=None):
		"""Makes the record readonly unless creating a new object."""
		if obj:
			return ('f',) + self.readonly_fields
		return self.readonly_fields


admin.site.register(Person, PersonAdmin)
admin.site.register(PeopleFile, PeopleFileAdmin)
