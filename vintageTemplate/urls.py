from django.conf.urls import patterns, include, url
# from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Temporary login url for development. REMEMBER TO REMOVE LOGIN_REQIRED METHOD DECORATORS ON VIEWS!
    # url(r'^login/$', 'django.contrib.auth.views.login'),

    url(r'^', include('timeline.urls')),
    url(r'^', include('people.urls')),
    url(r'^', include('organizations.urls')),
    url(r'^', include('articles.urls')),

    # Uncomment the next line to allow admin access
    url(r'^admin/', include(admin.site.urls)),
    
    # The static url is for local development only!
) #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'vintage2018.views.handler404'