__author__ = 'redrush'

from django import template
from main.models import MediaCategory
from django.utils import translation

register = template.Library()

def nav_categorieslist():
    objects = MediaCategory.objects.filter(language=translation.get_language())
    return {'objects': objects}

register.inclusion_tag('nav_categorieslist.html')(nav_categorieslist)
