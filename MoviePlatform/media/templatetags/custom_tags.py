from django import template

from media.models import Media

register = template.Library()


@register.simple_tag
def media_count():
    return Media.objects.count()


@register.inclusion_tag('top_rated_media.html')
def top_rated_media():
    top_media = Media.objects.top_rated()[:5]
    return {'top_media': top_media}


@register.filter(name='rating_to_stars')
def rating_to_stars(value):
    return '⭐' * value
