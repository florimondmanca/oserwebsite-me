"""Internal site context processors."""

from django.utils.functional import SimpleLazyObject
from .utils import get_profile_or_none


def profile(request):
    """Make the user profile available to template, if exists."""
    def get_profile():  # only evaluated when {{ profile }} is in template
        return get_profile_or_none(request.user)
    return {'profile': SimpleLazyObject(get_profile)}
