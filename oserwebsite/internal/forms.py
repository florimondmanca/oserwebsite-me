"""Internal site forms."""

from django import forms
from django.contrib.auth.models import User
from django.utils.html import mark_safe

from .models import Student, TutoringGroup, Tutor


class RegisterForm(forms.Form):
    """Form for user registration."""

    STUDENT = 'ST'
    TUTOR = 'TU'
    ROLE_CHOICES = (
        (STUDENT, 'Lycéen'),
        (TUTOR, 'Tuteur'),
    )

    first_name = forms.CharField(label='Prénom', max_length=100)
    last_name = forms.CharField(label='Nom', max_length=100)
    email = forms.EmailField(label='Adresse électronique', max_length=100,
                             help_text="Elle vous servira d'identifiant.")
    password = forms.CharField(label='Mot de passe',
                               widget=forms.PasswordInput,
                               min_length=8,
                               max_length=100)
    role = forms.ChoiceField(label="M'inscrire en tant que...",
                             choices=ROLE_CHOICES)

    user_exists_error = mark_safe(
        "Un compte associé à cette adresse électronique existe déjà ! "
        "<i class='em em-cold_sweat'></i>")

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(username=email)
            raise forms.ValidationError(self.user_exists_error)
        except User.DoesNotExist:
            pass
        return email


class AddressFormMixin(forms.Form):
    """Form for an address."""

    def clean_line1(self):
        return self.cleaned_data['line1'].upper()

    def clean_line2(self):
        return self.cleaned_data['line2'].upper()

    def clean_post_code(self):
        post_code = self.cleaned_data['post_code']
        post_code = post_code.replace(' ', '')
        try:
            int(post_code)
        except ValueError:
            raise forms.ValidationError({
                'post_code': "Le code postal doit être numérique."
            })
        return post_code

    class Meta:  # noqa
        fields = (
            'line1', 'line2', 'post_code', 'city', 'country',
        )


class ProfileForm(forms.Form):
    """Abstract base form for profile registration."""

    class Meta:  # noqa
        fields = (
            'birthday', 'phone',
            'user',
        )
        widgets = {
            'user': forms.HiddenInput(),
        }


class StudentProfileForm(AddressFormMixin, forms.ModelForm):
    """Form for student profile registration."""

    class Meta:  # noqa
        model = Student
        fields = (
            *AddressFormMixin.Meta.fields,
            *ProfileForm.Meta.fields,
            'high_school', 'level', 'branch',
            'tutoring_group',
        )
        widgets = {
            **ProfileForm.Meta.widgets,
            'tutoring_group': forms.HiddenInput(),
        }

    def compute_tutoring_group(self):
        high_school = self.cleaned_data['high_school']
        level = self.cleaned_data['level']
        tutoring_group, create = TutoringGroup.objects.get_or_create(
            high_school=high_school,
            level=level)
        return tutoring_group

    def clean_tutoring_group(self):
        return self.compute_tutoring_group()


class TutorProfileForm(AddressFormMixin, forms.ModelForm):
    """Form for tutor profile registration."""

    class Meta:  # noqa
        model = Tutor
        fields = (
            *ProfileForm.Meta.fields,
            'tutoring_group',
        )
        widgets = {
            **ProfileForm.Meta.widgets,
        }
