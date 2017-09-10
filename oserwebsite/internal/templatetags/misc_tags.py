"""Miscellaneous template tags."""
from django import template
from django.apps import apps

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


@register.inclusion_tag('misc/model_table.html')
def model_table(name, *fields, app_label='internal'):
    """Render a simple Bootstrap table for model.

    Parameters
    ----------
    model : str
        Name of the model (case insensitive, uses django.apps.get_model
        under the hood).
    fields : varargs of str
        List of fields shown as table columns.
    """
    model = apps.get_model(app_label, name)
    items = model.objects.all().values_list(*fields)
    field_names = [model._meta.get_field(field).verbose_name
                   for field in fields]
    return {'items': items, 'fields': field_names}
