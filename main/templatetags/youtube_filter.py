from django import template
from urlparse import parse_qs
from django.template.defaultfilters import stringfilter

register = template.Library()
import re

@register.filter(name='youtube_embed_url')
# converts youtube URL into embed HTML
# value is url
def youtube_embed_url(value):
    qs = value.split('?')
    video_id = parse_qs(qs[1])['v'][0]
    if video_id:
        embed_url = 'http://www.youtube.com/embed/%s' %video_id
        res = "<iframe width=\"560\" height=\"315\" src=\"%s\" frameborder=\"0\" allowfullscreen></iframe>" %(embed_url)
        return res
    return ''

youtube_embed_url.is_safe = True


@stringfilter
def youthumbnail(value, args):
    '''returns youtube thumb url
    args s, l (small, large)'''
    qs = value.split('?')
    video_id = parse_qs(qs[1])['v'][0]

    if args == 's':
        return "http://img.youtube.com/vi/%s/2.jpg" % video_id
    elif args == 'l':
        return "http://img.youtube.com/vi/%s/0.jpg" % video_id
    else:
        return None

register.filter('youthumbnail', youthumbnail)