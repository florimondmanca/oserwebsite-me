"""Card components."""

from django import template

register = template.Library()


@register.inclusion_tag('internal/components/card_list.html')
def card_list(title, queryset, empty=""):
    """Render a card with title and list of items."""
    return {'title': title, 'items': queryset.all(), 'empty_msg': empty}


@register.inclusion_tag('internal/components/card_list_count.html')
def card_list_count(title, queryset, empty=""):
    """Render a card with title, item count badge and list of items."""
    return {**card_list(title, queryset, empty), 'count': queryset.count()}
