"""Internal website views."""

from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import generic, View

from .models import Tutoree, Tutor, HighSchool, TutoringGroup
from .forms import RegisterForm


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
    """Detail of a tutoree."""

    model = Tutoree
    context_object_name = 'tutoree'


class TutorDetailView(LoginRequiredMixin, generic.DetailView):
    """Detail of a tutor."""

    model = Tutor
    context_object_name = 'tutor'


class HighSchoolDetailView(LoginRequiredMixin, generic.DetailView):
    """Detail of a high school."""

    model = HighSchool
    context_object_name = 'high_school'


class HighSchoolListView(LoginRequiredMixin, generic.ListView):
    """List of the high schools."""

    model = HighSchool
    context_object_name = 'high_school_list'


class TutoringGroupDetailView(LoginRequiredMixin, generic.DetailView):
    """Detail of a tutoring group."""

    model = TutoringGroup
    context_object_name = 'tutoring_group'


class TutoringGroupListView(LoginRequiredMixin, generic.ListView):
    """List of the tutoring groups."""

    model = TutoringGroup
    context_object_name = 'tutoring_group_list'


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # user = User.objects.create_user(
            #     username=email,
            #     password=password,
            #     email=email,
            #     first_name=first_name,
            #     last_name=last_name,
            # )
            messages.success(request,
                             "Le nouvel utilisateur a été créé, "
                             "vous pouvez maintenant vous connecter.")
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'internal/register.html', {'form': form})
