"""Utility template tags."""


from django import template

register = template.Library()


@register.inclusion_tag('utils/icon.html')
def icon(code):
    """Render a favicon span element."""
    return {'code': code}
