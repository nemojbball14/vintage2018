from django.contrib import admin
from organizations.models import Organization, OrganizationType, OrganizationPicture, OrganizationSpecial, OrganizationSpecialPicture


class OrganizationTypeAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ("name",)} 
	list_display = ('name',)
	fields = ('name', 'slug')


class OrganizationAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ("name",)} 
	list_display = ('name',)
	fields = ('org_type', 'name', 'slug', 'people',)
	list_filter = ['org_type',]
	filter_horizontal = ('people',)


class OrganizationPictureAdmin(admin.ModelAdmin):
	list_display = ('org', 'pic',)
	fields = ('org', 'pic',)
	list_filter = ['org',]


class OrganizationSpecialAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ("name",)} 
	list_display = ('name',)
	fields = ('name', 'slug', 'people',)


class OrganizationSpecialPictureAdmin(admin.ModelAdmin):
	list_display = ('org', 'pic',)
	fields = ('org', 'pic',)
	list_filter = ['org',]


admin.site.register(OrganizationType, OrganizationTypeAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(OrganizationPicture, OrganizationPictureAdmin)
admin.site.register(OrganizationSpecial, OrganizationSpecialAdmin)
admin.site.register(OrganizationSpecialPicture, OrganizationSpecialPictureAdmin)
