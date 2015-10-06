
from django import template
from moody.models import Album

register = template.Library()

@register.inclusion_tag('moody/arts.html')
def get_album_list(als=None):
    return {'als': Album.objects.all(), 'act_als': als}