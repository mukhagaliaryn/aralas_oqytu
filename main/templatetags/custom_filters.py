from django import template
import re
register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def youtube_id(url):

    if not url:
        return ''
    pattern = r'(?:v=|\/embed\/|\/\d+\/|\/vi\/|youtu\.be\/|\/v\/|\/e\/|watch\?v=|&v=)([^#&?\/\s]{11})'
    match = re.search(pattern, url)
    return match.group(1) if match else ''


@register.filter
def range_filter(value):
    return range(value)
