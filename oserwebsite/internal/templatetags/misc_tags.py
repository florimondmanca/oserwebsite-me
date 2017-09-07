"""Miscellaneous template tags."""
from django import template

register = template.Library()


@register.inclusion_tag('misc/icon.html')
def icon(code, *options):
    """Render a favicon span element.

    Parameters
    ----------
    code : str
        FontAwesome icon code (e.g. 'lock', 'user', 'clock-o', etc.)
    options : optional
        Any number of FontAwesome-compatible options.
        e.g. pass 'fw' for 'fa-fw', 'spin' for 'fa-spin', 'pull-right'
        for 'fa-pull-right', etc.
    """
    context = {'code': code}
    context['fa_classes'] = ' '.join('fa-{}'.format(opt) for opt in options)
    return context
