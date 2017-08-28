"""Internal website context processors."""

from .models import Tutoree, Tutor


def high_school(request):
    """Make the user's high school available to a template."""
    # TODO : improve the flexibility of this...
    # (what if the user is neither a tutor or a tutoree?)
    if request.user.is_authenticated():
        user = request.user
        try:
            tutoree = Tutoree.objects.get(user=user)
        except Tutoree.DoesNotExist:
            pass
        else:
            return {'high_school': tutoree.high_school}
        try:
            tutor = Tutor.objects.get(user=user)
        except Tutor.DoesNotExist:
            pass
        else:
            return {'high_school': tutor.high_school}
    return {'high_school': None}
