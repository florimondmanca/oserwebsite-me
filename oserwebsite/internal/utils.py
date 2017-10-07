"""Utility functions."""

from smtplib import SMTPAuthenticationError

from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages

from .models import Tutor, Student


def get_profile_or_none(user):
    """Return the profile of the user, if exists, else None."""
    if not user:
        return None
    if user.is_authenticated():
        profile = Student.objects.filter(user=user).first()
        if not profile:
            profile = Tutor.objects.filter(user=user).first()
        return profile
    else:
        return None


def send_email_safe(request, subject, message, email_from, email_to,
                    success_msg=None, error_msg=None):
    """Send an email with success and error management.

    request :
        Django's view request parameter.
    subject, message, email_from, email_to :
        Django's send_mail() parameters.
    success_msg : str
        Success message that will be displayed on success through
        Django's messages API. A standard, polite default message is used
        by default.
    error_msg : str
        Error message that will be displayed on error (bad header) through
        Django's messages API.
        A standard, polite error message is used by default.
    """
    if success_msg is None:
        success_msg = (
            "Votre message a bien été envoyé. "
            "Nous y répondrons dès que possible !")
    if error_msg is None:
        error_msg = ("Oups ! Une erreur s'est produite lors de "
                     "l'envoi du message... "
                     "Veuillez réessayer dans quelques instants.")
    try:
        send_mail(subject, message, email_from, email_to)
        if success_msg:
            messages.success(request, success_msg)
        return True
    except BadHeaderError:
        messages.error(request, error_msg)
    except SMTPAuthenticationError:
        messages.error(request,
                       "Le serveur d'envoi semble indisponible. "
                       "Veuillez contacter le webmaster pour signaler le "
                       "problème. ")
        return False
