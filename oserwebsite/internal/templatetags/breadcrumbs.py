"""Breadcrumbs template tag.

See https://www.djangosnippets.org/snippets/1289/.
"""
from django import template
from django.shortcuts import reverse
from django.urls import NoReverseMatch

register = template.Library()


@register.inclusion_tag('breadcrumb/url.html')
def breadcrumb_url(title, name, *args):
    """Include a Bootstrap li breadcrumb-item element containing a link.

    Parameters
    ----------
    title : str
        The title displayed on the breadcrumb.
    name : str
        The name of the view as defined in urls.py.
        The tag will try to reverse based on this name. It is safe to
        pass a non-existing view name ("#" will be used to avoid crashing).
    args : args
        Other arguments passed to reverse(view_name, args=args).

    Examples
    --------
    {% breadcrumb_url title="Home" name="index %"}
    {% breadcrumb_url title="Home" {% url index %} %}

    """
    try:
        url = reverse(name, args=args)
    except NoReverseMatch:
        url = "#"
    return {'title': title, 'url': url, }


@register.inclusion_tag('breadcrumb/default.html')
def breadcrumb(title):
    """Include a Bootstrap li breadcrumb-item element.

    Parameters
    ----------
    title : str
        The title displayed on the breadcrumb.
    Examples
    --------
    {% breadcrumb "Home" %}
    {% breadcrumb "Products" %}

    """
    return {'title': title, }


@register.inclusion_tag('breadcrumb/active.html')
def breadcrumb_active(title):
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
    return breadcrumb(title)
