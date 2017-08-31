"""Breadcrumbs template tag.

See https://www.djangosnippets.org/snippets/1289/.
"""
from django import template
from django.shortcuts import reverse
from django.urls import NoReverseMatch

register = template.Library()


@register.inclusion_tag('breadcrumb/url.html')
def breadcrumb_url(name, view_name, *args):
    """Include a Bootstrap li breadcrumb-item element containing a link.

    Parameters
    ----------
    name : str
        The name displayed on the breadcrumb.
    view_name : str
        The name of the view to the link.
        The tag will try to reverse based on this name. If fails, the
        url used will be "#" to avoid crashing.
    args : args
        Other arguments passed to reverse(view_name, args=args).

    Examples
    --------
    {% breadcrumb_url "Home" "index %"}
    {% breadcrumb_url {% url index %} %}

    """
    try:
        view_url = reverse(view_name, args=args)
    except NoReverseMatch:
        view_url = "#"
    return {'name': name, 'url': view_url, }


@register.inclusion_tag('breadcrumb/default.html')
def breadcrumb(name):
    """Include a Bootstrap li breadcrumb-item element.

    Parameters
    ----------
    name : str
        The name displayed on the breadcrumb.
    Examples
    --------
    {% breadcrumb "Home" %}
    {% breadcrumb "Products" %}

    """
    return {'name': name, }


@register.inclusion_tag('breadcrumb/active.html')
def breadcrumb_active(name):
    """Render a Bootstrap active breadcrumb item.

    Parameters
    ----------
    name : str
        The name displayed on the breadcrumb.
    Examples
    --------
    {% breadcrumb_active "Home" %}
    {% breadcrumb_active "Products" %}

    """
    return {'name': name, }
