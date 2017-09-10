"""Cards-related template tags."""

from django import template

register = template.Library()


@register.inclusion_tag('cards/cardlist.html')
def cardlist(queryset=None, title="", empty="", scroll=None, count=False,
             item_template="cards/cardlist_item.html", limit=None,
             all_url="", icon=None):
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
        Pass True or 1 to use the default scroll value (300px).
        e.g. : scroll="300px", scroll=True
    item_template : str, optional
        Name of the template to use when rendering the list items.
        Item template is included inside the <li></li> tags.
        Default template is just rendering the item directly.
    count : bool, optional
        Pass True to display the number of items in a badge alongside
        the card title.
    limit : int, optional
        The maximum number of items to display in the list.
        Default behavior is to display all elements in the list.
    all_url : str, optional
        The absolute url used when more than `limit` items are in the
        list.
    icon : str, optional
        Name of a FontAwesome icon to display on the upper right corner
        of the card header. e.g. 'calendar', 'users', 'o-clock', etc.
    """
    if not empty:
        if title:
            empty = "Pas de {}.".format(title.lower())
        else:
            empty = "Aucune données."
    if queryset:
        items = queryset.all()
        count = count and queryset.count()
    else:
        items = []
        count = 0
    if scroll in (True, 1):
        scroll = "300px"
    return {
        'title': title,
        'items': items,
        'empty_msg': empty,
        'scroll': scroll,
        'item_template': item_template,
        'count': count,
        'limit': limit or float('inf'),
        'all_url': all_url or '#',
        'icon': icon,
    }
