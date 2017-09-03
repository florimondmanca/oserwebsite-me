"""Internal website views."""

from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import generic, View

from .models import Student, Tutor, HighSchool, TutoringGroup
from .forms import RegisterForm


class IndexView(LoginRequiredMixin, generic.TemplateView):
    """Home index view."""

    template_name = 'internal/index.html'


class RegisterView(View):
    """Register view."""

    template_name = 'registration/register.html'
    success_message = ("L'utilisateur {} a été créé. "
                       "Vous pouvez maintenant vous connecter avec "
                       "vos nouveaux identifiants.")

    def get(self, request):
        form = RegisterForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = {k: form.cleaned_data[k]
                    for k in ('first_name', 'last_name', 'email', 'password')}
            # User.objects.create_user(username=data['email'], **data)
            role = form.cleaned_data['role']
            more_info = {
                form.TUTOR: 'register-tutor',
                form.TUTOREE: 'register-student',
            }
            return redirect('index')
        return render(request, self.template_name, {'form': form})


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


class StudentDetailView(LoginRequiredMixin, generic.DetailView):
    """Detail of a student."""

    model = Student
    context_object_name = 'student'


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
