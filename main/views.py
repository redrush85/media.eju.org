# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404, RequestContext 
from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from main.models import *
from django.utils import translation
from django.views.decorators.cache import cache_page
from sorl.thumbnail import get_thumbnail
import json
from django.core import serializers

# Create your views here.
media_per_page = 6

@cache_page(60 * 10)
def index(request):
    lastalbums = MediaAlbum.objects.filter(is_active=True, language=translation.get_language()).order_by('-created_at')[:6]
    lastvideos = MediaVideoNode.objects.filter(is_active=True, language=translation.get_language()).order_by('-created_at')[:6]
    lastphotos = MediaPhotoNode.objects.filter(is_active=True, language=translation.get_language()).order_by('-created_at')[:6]
    return render_to_response("index.html", {'lastalbums': lastalbums, 'lastvideos': lastvideos, 'lastphotos': lastphotos }, context_instance=RequestContext(request))

@cache_page(60 * 10)
def getvideo(request, slug):
    video = get_object_or_404(MediaVideoNode, slug=slug)
    return render_to_response("page_video.html", {'video': video}, context_instance=RequestContext(request))

@cache_page(60 * 10)
def getphoto(request, slug):
    photo = get_object_or_404(MediaPhotoNode, slug=slug)
    return render_to_response("page_photo.html", {'photo': photo}, context_instance=RequestContext(request))

@cache_page(60 * 10)
def getphotocategory(request, id):
    category = get_object_or_404(MediaCategory, id=id)
    photos = MediaPhotoNode.objects.filter(category_id=id, is_active=1, language=translation.get_language()).order_by('-created_at')
    paginator = Paginator(photos, media_per_page)
    page = request.GET.get('page')
    try:
        photos = paginator.page(page)
    except PageNotAnInteger:
        photos = paginator.page(1)
    except EmptyPage:
        photos = paginator.page(paginator.num_pages)
    return render_to_response("photo_category.html", {'photos': photos, 'category': category}, context_instance=RequestContext(request))

@cache_page(60 * 10)
def getallphotos(request):
    photos = MediaPhotoNode.objects.filter(is_active=1, language=translation.get_language()).order_by('-created_at')
    paginator = Paginator(photos, media_per_page)
    page = request.GET.get('page')
    try:
        photos = paginator.page(page)
    except PageNotAnInteger:
        photos = paginator.page(1)
    except EmptyPage:
        photos = paginator.page(paginator.num_pages)
    return render_to_response("allphotos.html", {'photos': photos}, context_instance=RequestContext(request))

@cache_page(60 * 10)
def getallvideos(request):
    video_list = MediaVideoNode.objects.filter(is_active=1, language=translation.get_language()).order_by('-created_at')
    paginator = Paginator(video_list, media_per_page)
    page = request.GET.get('page')
    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        videos = paginator.page(1)
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)
    return render_to_response("allvideos.html", {'videos': videos}, context_instance=RequestContext(request))

@cache_page(60 * 10)
def getallalbums(request):
    album_list = MediaAlbum.objects.filter(is_active=1, language=translation.get_language()).order_by('-created_at')
    paginator = Paginator(album_list, media_per_page)
    page = request.GET.get('page')
    try:
        albums = paginator.page(page)
    except PageNotAnInteger:
        albums = paginator.page(1)
    except EmptyPage:
        albums = paginator.page(paginator.num_pages)
    return render_to_response("allalbums.html", {'albums': albums}, context_instance=RequestContext(request))

@cache_page(60 * 10)
def getalbum(request, slug):
    album = get_object_or_404(MediaAlbum, slug=slug)
    photos = album.images.all()
    paginator = Paginator(photos, media_per_page)
    page = request.GET.get('page')
    try:
        photos = paginator.page(page)
    except PageNotAnInteger:
        photos = paginator.page(1)
    except EmptyPage:
        photos = paginator.page(paginator.num_pages)
    return render_to_response("page_album.html", {'photos': photos, 'album': album}, context_instance=RequestContext(request))

    
def _api_resources(api):
  resources = {}
  api_name = api.api_name

  for name in sorted(api._registry.keys()):
    resource = api._registry[name]
    resources[name] = {
      'list_endpoint': api._build_reverse_url("api_dispatch_list", kwargs={
        'api_name': api_name,
        'resource_name': name,
      }),
      'schema': api._build_reverse_url("api_get_schema", kwargs={
        'api_name': api_name,
        'resource_name': name,
      }),
      'doc': resource.__doc__,
      'resource': resource
    }
  return resources


def apibrowse(request, api):
  resources = _api_resources(api)
  return TemplateResponse(request, 'tasty_browser/index.html', {
    'api': api,
    'resources': resources
  })
  
def getimage(request):
  response_data = {}
  response_data = {'result':'error',
                   'message':'image not found'}
  
  if request.GET.get('image_id'):
    image_id = request.GET.get('image_id')
    photo = get_object_or_404(MediaPhotoNode, id=image_id)
    response_data = {'result': 'ok',
                     'message': photo.preview()}
    
  return HttpResponse(json.dumps(response_data), mimetype="application/json")