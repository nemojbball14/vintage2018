from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	# temporary login url for development. REMEMBER TO REMOVE LOGIN_REQIRED METHOD DECORATORS ON VIEWS!
	url(r'^login/$', 'django.contrib.auth.views.login'),

	url(r'^', include('timeline.urls')),
    url(r'^', include('people.urls')),
    url(r'^', include('organizations.urls')),

    #uncomment the next line to allow admin access
    url(r'^admin/', include(admin.site.urls)),
    
    #the static url is for local development only!
) #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'vintage20xx.views.handler404'
