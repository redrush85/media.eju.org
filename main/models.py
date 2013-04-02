# -*- coding: utf-8 -*-
#from django.db import models
from django.conf import settings
from util import models
from sorl.thumbnail import get_thumbnail
from django.core.urlresolvers import reverse


# Create your models here.
class MediaCategory(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    language = models.CharField(max_length=15, choices=settings.LANGUAGES, default="en")

    class Meta:
        verbose_name_plural = 'Categories'

    def __unicode__(self):
        return self.title

class Tag(models.Model):
    word = models.CharField(max_length=35)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Tags'

    def __unicode__(self):
        return self.word

class MediaVideoNode(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(MediaCategory, related_name = 'category')
    description = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag,related_name='videos', blank=True)
    youtube_link = models.CharField(max_length=200, verbose_name="Youtube link")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(max_length=200, verbose_name="URL", unique=True)
    language = models.CharField(max_length=15, choices=settings.LANGUAGES, default="en")

    class Meta:
        verbose_name_plural = 'Videos'

    def __unicode__(self):
        return self.title

    def preview(self):
        if self.youtube_link:
            from urlparse import parse_qs
            qs = self.youtube_link.split('?')
            video_id = parse_qs(qs[1])['v'][0]
            return "<img src='http://img.youtube.com/vi/%s/2.jpg'/>" % video_id
        return ''
    preview.allow_tags = True

    def get_absolute_url(self):
        return reverse('viewvideo', args=[self.slug])

class MediaPhotoNode(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(MediaCategory)
    description = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag,related_name='photos', blank=True)
    image = models.ImageField(upload_to="images/")
    created_at  = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(max_length=200, verbose_name="URL", unique=True)
    language = models.CharField(max_length=15, choices=settings.LANGUAGES, default="en")


    class Meta:
        verbose_name_plural = 'Photos'


    def preview(self):
        if self.image:
            #return '<img src="/media/%s"  width="180px" height="153px" />' % self.image
            img_path = get_thumbnail(self.image, '107x80', crop='center', quality=90)
            return u'<img src="/media/%s" />' % img_path
        return ''
    preview.allow_tags = True

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('viewphoto', args=[self.slug])

class MediaAlbum(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    albumimage = models.ImageField(upload_to="images/album_media", verbose_name="Cover")
    images = models.ManyToManyField(MediaPhotoNode)
    created_at  = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(max_length=200, verbose_name="URL", unique=True)
    language = models.CharField(max_length=15, choices=settings.LANGUAGES, default="en")

    class Meta:
        verbose_name_plural = 'Albums'


    def preview(self):
        if self.albumimage:
            img_path = get_thumbnail(self.albumimage, '107x80', crop='center', quality=90)
            return u'<img src="/media/%s" />' % img_path
        return ''
    preview.allow_tags = True

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('viewalbum', args=[self.slug])

