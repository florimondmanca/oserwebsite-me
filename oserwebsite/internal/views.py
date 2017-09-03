"""Internal website views."""

from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import generic, View

from .models import Student, Tutor, HighSchool, TutoringGroup
from .forms import RegisterForm, RegisterStudentForm


class IndexView(LoginRequiredMixin, generic.TemplateView):
    """Home index view."""

    template_name = 'internal/index.html'


class RegisterView(View):
    """Register view."""

    template_name = 'internal/register.html'

    def get(self, request):
        form = RegisterForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = {k: form.cleaned_data[k]
                    for k in ('first_name', 'last_name', 'email', 'password')}
            user = User.objects.create_user(username=data['email'], **data)
            role = form.cleaned_data['role']
            messages.success(request,
                             "L'utilisateur {} a été créé."
                             .format(user.username))
            messages.info(request,
                          "Veuillez compléter votre inscription ci-dessous.")
            if role == form.TUTOR:
                return redirect('register-tutor', pk=user.id)
            elif role == form.STUDENT:
                return redirect('register-student', pk=user.id)
        return render(request, self.template_name, {'form': form})


class RegisterStudentView(View):
    """Complementary register view for student."""

    template_name = 'internal/register_student.html'

    def get(self, request, pk):
        user = User.objects.get(id=pk)
        form = RegisterStudentForm(initial={'user': user})
        return render(request, self.template_name, {'form': form, 'pk': pk})

    def post(self, request, pk):
        user = User.objects.get(id=pk)
        student, create = Student.objects.get_or_create(user=user)
        form = RegisterStudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, self.template_name, {'form': form, 'pk': pk})


class RegisterTutorView(View):
    """Complementary register view for tutor."""
    pass


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
