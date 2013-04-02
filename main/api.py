# main/api.py
from tastypie.resources import ModelResource
from tastypie import fields
from main.models import MediaCategory, MediaVideoNode, MediaPhotoNode, MediaAlbum


class CategoryResource(ModelResource):
    class Meta:
        queryset = MediaCategory.objects.all()
        resource_name = 'category'

        filtering = {
           "language": ('exact',),
        }

        
class VideoResource(ModelResource):
    class Meta:
        queryset = MediaVideoNode.objects.all()
        resource_name = 'video'

        filtering = {
           "language": ('exact',),
        }

class PhotoResource(ModelResource):
    category = fields.ForeignKey('main.api.CategoryResource', 'category')

    class Meta:
        queryset = MediaPhotoNode.objects.all()
        resource_name = 'photo'

        filtering = {
            "category": ('exact',),
            "language": ('exact',),
        }
        
    def dehydrate(self, bundle):
      bundle.data['thumb'] = bundle.obj.preview()
      return bundle

class AlbumResource(ModelResource):
    images = fields.ToManyField('main.api.PhotoResource', 'images')
    class Meta:
        queryset = MediaAlbum.objects.all()
        resource_name = 'album'  
        
        filtering = {
           "language": ('exact',),
        }
