from haystack.indexes import *
from haystack import site
from main.models import MediaPhotoNode, MediaVideoNode, MediaAlbum


class PhotoIndex(SearchIndex):
    text = CharField(document=True, use_template=True)

class VideoIndex(SearchIndex):
    text = CharField(document=True, use_template=True)

class AlbumIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    
    #def index_queryset(self):
    #    """Used when the entire index for model is updated."""
    #    return MediaPhotoNode.objects.all()

site.register(MediaPhotoNode, PhotoIndex)
site.register(MediaVideoNode, VideoIndex)
site.register(MediaAlbum, AlbumIndex)


