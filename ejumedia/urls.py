from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
#tastypie
from tastypie.api import Api
from main.api import CategoryResource, VideoResource, PhotoResource, PhotoResource, AlbumResource
admin.autodiscover()


v1_api = Api(api_name="v1")
v1_api.register(CategoryResource())
v1_api.register(VideoResource())
v1_api.register(PhotoResource())
v1_api.register(AlbumResource())



urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'main.views.index', name='homepage'),
    url(r'^video/(?P<slug>[a-zA-Z0-9_.-]+)/$', 'main.views.getvideo', name='viewvideo'),
    url(r'^photo/(?P<slug>[a-zA-Z0-9_.-]+)/$', 'main.views.getphoto', name='viewphoto'),
    url(r'^album/(?P<slug>[a-zA-Z0-9_.-]+)/$', 'main.views.getalbum', name='viewalbum'),
    url(r'^category/(?P<id>\d+)/$', 'main.views.getphotocategory', name='viewphotocategory'),
    url(r'^videos/$', 'main.views.getallvideos', name='viewallvideos'),
    url(r'^photos/$', 'main.views.getallphotos', name='viewallphotos'),
    url(r'^albums/$', 'main.views.getallalbums', name='viewallalbums'),
    url(r'^getimage/$', 'main.views.getimage', name='getimage'),
    
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    #url(r'^grappelli/', include('grappelli.urls')),

    url(r'^search/', include('haystack.urls')),
    url(r'^admin/', include(admin.site.urls)),
    # dev media directory
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    #change language
    url(r'^i18n/', include('django.conf.urls.i18n')),
    #api
    url(r'^api/', include(v1_api.urls)),
    url(r'^api-doc/', 'main.views.apibrowse', {'api': v1_api}),
    
)
