#coding=utf-8
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
# import authority

# admin.autodiscover()
# authority.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'store_system.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'',include("role.urls")),
    url(r'^stock/',include("stock.urls")),
    url(r'^order/',include("order.urls")),
    # (r'^authority/', include('authority.urls')),
)+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )