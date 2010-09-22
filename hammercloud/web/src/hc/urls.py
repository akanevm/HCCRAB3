from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

  #If some application urls are needed to be 
  #added, add them here.
  #(r'^app/atlas', include('hc.atlas.urls'))

  (r'',                   include('hc.core.urls')          ),
  (r'',                   include('hc.core.base.rss.urls') ),
  (r'^admin/',            include(admin.site.urls)         ),

#  (r'^accounts/login/$',  'django.contrib.auth.views.login', {'template_name': 'core/app/login.html'}),
    
)

