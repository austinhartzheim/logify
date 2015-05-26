from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^webhooks/', include('webhooks.urls')),
    
    # Examples:
    # url(r'^$', 'logify.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
]
