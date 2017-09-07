"""Cards-related template tags."""

from django import template

register = template.Library()


@register.inclusion_tag('cards/cardlist.html')
def cardlist(queryset, title="", empty="", scroll=None, count=False,
             item_template="cards/cardlist_item.html", limit=None,
             all_url=""):
    """Render a card with title and list of items.

    If item provides get_absolute_url() method, item is rendered as a <a>
    instead of an <li>.

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
    item_template : str, optional
        Name of the template to use when rendering the list items.
        Item template is included inside the <li></li> tags.
        Default template is just rendering the item directly.
    count : bool, optional
        Pass True to display the number of items in a badge alongside
        the card title.
    """
    if not empty:
        if title:
            empty = "Pas de {}.".format(title.lower())
        else:
            empty = "Aucune données."
    if count:
        count = queryset.count()
    if not limit:
        limit = float('inf')
    return {
        'title': title,
        'items': queryset.all(),
        'empty_msg': empty,
        'scroll': scroll,
        'item_template': item_template,
        'count': count,
        'limit': limit,
        'all_url': all_url,
    }
