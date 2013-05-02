__author__ = 'redrush'

from django.contrib import admin
from main.models import *
from sorl.thumbnail.admin import AdminImageMixin

class MediaCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'language')
    ordering = ('id',)
    list_filter = ('language', )

class TagAdmin(admin.ModelAdmin):
    list_display = ('word',)
    ordering = ('-id',)
    list_per_page = 20

class MediaVideoNodeAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'description', 'preview', 'created_at', 'is_active', 'language')
    ordering = ('-id',)
    list_filter = ('category', 'created_at', 'language')
    list_per_page = 20
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title']
    date_hierarchy = 'created_at'

class MediaPhotoNodeAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('title', 'category', 'preview', 'created_at', 'is_active', 'language')
    ordering = ('-id',)
    list_filter = ('category', 'created_at', 'language')
    list_per_page = 20
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title']
    date_hierarchy = 'created_at'

class MediaAlbumAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('title', 'preview', 'created_at', 'is_active', 'language')
    ordering = ('-id',)
    #raw_id_fields = ('images',)
    filter_horizontal = ('images',)
    list_per_page = 20
    list_filter = ('created_at', 'language')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title']
    date_hierarchy = 'created_at'



admin.site.register(MediaCategory, MediaCategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(MediaVideoNode, MediaVideoNodeAdmin)
admin.site.register(MediaPhotoNode, MediaPhotoNodeAdmin)
admin.site.register(MediaAlbum, MediaAlbumAdmin)