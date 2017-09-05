"""Card components."""

from django import template

register = template.Library()


@register.inclusion_tag('components/cardlist.html')
def cardlist(queryset, title="", empty="", scroll=None):
    """Render a card with title and list of items.

    Parameters
    ----------
    queryset : QuerySet
        List of items to render.
    title : str, optional
        Title of the card (no title by default).
    empty : str, optional
        Text to display in list group if not items in queryset
        (default text is infered from list title if given).
    scroll : str, optional
        Provide a CSS min-height property value to make the
        list group y-scrollable (no value by default).
        e.g. : scroll="300px", scroll="100em"
    """
    if not empty:
        if title:
            empty = "Pas de {}.".format(title.lower())
        else:
            empty = "Aucune données."
    return {
        'title': title,
        'items': queryset.all(),
        'empty_msg': empty,
        'scroll': scroll,
    }


@register.inclusion_tag('components/cardlist_count.html')
def cardlist_count(queryset, **kwargs):
    """Render a card with title, item count badge and list of items.

    Parameters
    ----------
    queryset : QuerySet
        List of items to render.
    title : str, optional
        Title of the card (no title by default).
    empty : str, optional
        Text to display in list group if not items in queryset
        (default text is infered from list title if given).
    scroll : str, optional
        Provide a CSS min-height property value to make the
        list group y-scrollable (no value by default).
        e.g. : scroll="300px", scroll="100em"
    """
    return {**cardlist(queryset, **kwargs), 'count': queryset.count()}
