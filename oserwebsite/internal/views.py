"""Internal website views."""

import random

from django.shortcuts import render
from django.views import generic
from .models import Tutoree, Tutor


def index(request):
    """Home page/dashboard."""
    tutoree = random.choice(Tutoree.objects.all())
    upcoming_meetings = tutoree.tutoring_group.tutoringmeeting_set.all()[:5]

    return render(request, 'internal/index.html', {
        'tutoree': tutoree,
        'missing_documents': False,
        'meetings': upcoming_meetings,
    })


class TutoreeDetailView(generic.DetailView):
    """Detail view for Tutoree."""

    model = Tutoree


class TutorDetailView(generic.DetailView):
    """Detail view for Tutor."""

    model = Tutor
