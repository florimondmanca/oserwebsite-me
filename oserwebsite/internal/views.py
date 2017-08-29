"""Internal website views."""

from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import ContextMixin
from django.views import generic, View
from .models import Tutoree, Tutor, HighSchool, TutoringMeeting, TutoringGroup
from .utils import get_profile_or_none


class IndexView(LoginRequiredMixin, ContextMixin, View):
    """Home page dashboard."""

    def get(self, request):
        profile = get_profile_or_none(request.user)
        if not profile:
            raise ValueError('Profile does not exist for user {}'
                             .format(request.user))
        upcoming_meetings = TutoringMeeting.objects.filter(
            tutoring_group=profile.tutoring_group)[:5]

        return render(request, 'internal/index.html', {
            'meetings': upcoming_meetings
        })


class BrandView(View):
    """View visited on clicking the brand."""

    def get(self, request):
        if request.user and request.user.is_authenticated():
            return redirect('index')
        else:
            return redirect('login')


class TutoreeDetailView(LoginRequiredMixin, generic.DetailView):
    """Detail view for Tutoree."""

    model = Tutoree


class TutorDetailView(LoginRequiredMixin, generic.DetailView):
    """Detail view for Tutor."""

    model = Tutor


class HighSchoolDetailView(LoginRequiredMixin, generic.DetailView):
    """Detail view for HighSchool."""

    model = HighSchool


class TutoringGroupDetailView(LoginRequiredMixin, generic.DetailView):
    """Detail view for TutoringGroup."""

    model = TutoringGroup
