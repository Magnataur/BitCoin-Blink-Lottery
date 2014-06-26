from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()



urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bcblink.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'blink_web.views.index'),
    url(r'^login/', 'blink_web.views.login'),
    url(r'^test/', 'blink_web.views.test'),
    url(r'^logout/', 'blink_web.views.logout'),
    url(r'^join/(\d+)/(\d+)/$', 'blink_web.views.join'),
    url(r'^blink/(\d+)/$', 'blink_web.views.blink'),
    url(r'^admin/', include(admin.site.urls)),
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
)
