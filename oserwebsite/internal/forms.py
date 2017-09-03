"""Internal site forms."""

from django import forms
from django.contrib.auth.models import User
from django.utils.html import mark_safe


class RegisterForm(forms.Form):
    """Form to register a tutor."""

    TUTOREE = 0
    TUTOR = 1
    CATEGORY_CHOICES = (
        (TUTOREE, 'Lycéen'),
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
    category = forms.ChoiceField(label="M'inscrire en tant que...",
                                 choices=CATEGORY_CHOICES)

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
