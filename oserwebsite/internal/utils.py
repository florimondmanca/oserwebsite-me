"""Utility functions."""

from .models import Tutor, Tutoree


def get_profile_or_none(user):
    """Return the profile of the user, if exists, else None."""
    if not user:
        return None
    if user.is_authenticated():
        profile = Tutoree.objects.filter(user=user).first()
        if not profile:
            profile = Tutor.objects.filter(user=user).first()
        return profile
    else:
        return None
