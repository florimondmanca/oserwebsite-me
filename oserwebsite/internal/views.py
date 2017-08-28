"""Internal website views."""

import random

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .models import Tutoree, Tutor, HighSchool


@login_required
def index(request):
    """Home page/dashboard."""
    tutoree = random.choice(Tutoree.objects.all())
    upcoming_meetings = tutoree.tutoring_group.tutoringmeeting_set.all()[:5]

    return render(request, 'internal/index.html', {
        'tutoree': tutoree,
        'missing_documents': False,
        'meetings': upcoming_meetings,
    })


class TutoreeDetailView(LoginRequiredMixin, generic.DetailView):
    """Detail view for Tutoree."""

    model = Tutoree


class TutorDetailView(LoginRequiredMixin, generic.DetailView):
    """Detail view for Tutor."""

    model = Tutor


class HighSchoolDetailView(LoginRequiredMixin, generic.DetailView):
    """Detail view for HighSchool."""

    model = HighSchool
