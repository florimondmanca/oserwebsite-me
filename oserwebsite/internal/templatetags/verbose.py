"""Template tags for accessing verbose names."""
from django import template

register = template.Library()


@register.simple_tag
def field_name(value, field):
    """Return the verbose name of a model's field."""
    if hasattr(value, 'model'):
        value = value.model

    return value._meta.get_field(field).verbose_name.title()
