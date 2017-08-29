"""Internal website views."""

from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic, View
from .models import Tutoree, Tutor, HighSchool, TutoringGroup


class IndexView(LoginRequiredMixin, generic.TemplateView):
    """Home index view."""

    template_name = 'internal/index.html'


class FaqView(LoginRequiredMixin, generic.TemplateView):
    """FAQ view."""

    template_name = 'internal/faq.html'


class BrandView(View):
    """View visited when clicking the brand."""

    def get(self, request):
        if request.user and request.user.is_authenticated():
            return redirect('index')
        else:
            return redirect('login')


class TutoreeDetailView(LoginRequiredMixin, generic.DetailView):
    """Detail view for Tutoree."""

    model = Tutoree
    context_object_name = 'tutoree'


class TutoreeListView(LoginRequiredMixin, generic.ListView):
    """List view for Tutoree."""

    model = Tutoree
    context_object_name = 'tutoree_list'


class HighSchoolTutoreeListView(LoginRequiredMixin, generic.ListView):
    """List view for Tutorees of a specific high school."""

    model = Tutoree
    template_name = 'internal/high_school_tutoree_list.html'
    context_object_name = 'tutoree_list'

    def get_queryset(self):
        return (Tutoree.objects
                .filter(high_school__id=self.kwargs['pk']))

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        high_school = HighSchool.objects.get(id=self.kwargs['pk'])
        context_data['high_school'] = high_school
        return context_data


class TutorDetailView(LoginRequiredMixin, generic.DetailView):
    """Detail view for Tutor."""

    model = Tutor
    context_object_name = 'tutor'


class HighSchoolDetailView(LoginRequiredMixin, generic.DetailView):
    """Detail view for HighSchool."""

    model = HighSchool
    context_object_name = 'high_school'


class TutoringGroupDetailView(LoginRequiredMixin, generic.DetailView):
    """Detail view for TutoringGroup."""

    model = TutoringGroup
    context_object_name = 'tutoring_group'
