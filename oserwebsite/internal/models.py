"""Models are defined here."""

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
import datetime


class AddressMixin(models.Model):
    """Mixin that adds address-related fieldsto a Model.

    Properties
    ----------
    address : str
        A multiline string displaying the full address.
    address_inline : str
        A string displaying the full address, made to be used inline.
    """

    line1 = models.CharField(
        'adresse (ligne 1)', max_length=100,
        help_text="Numéro, rue, voie, nom de société, etc.")
    line2 = models.CharField(
        'adresse (ligne 2)', max_length=100, blank=True,
        help_text="Bâtiment, étage, lieu-dit, etc.")
    post_code = models.CharField(
        'code postal', max_length=20)
    city = models.CharField('ville', max_length=50)
    country = models.ForeignKey('Country',
                                models.SET_NULL, null=True,
                                verbose_name='pays')

    def _address_separated(self, sep=', '):
        city_line = '{} {}'.format(self.post_code, self.city.upper())
        _lines = (self.line1, self.line2, city_line,
                  self.country.name.upper())
        lines = list(filter(None, _lines))
        return mark_safe(sep.join(lines))

    @property
    def address_inline(self):
        return self._address_separated(sep=', ')

    @property
    def address(self):
        return self._address_separated(sep='<br/>')


class Profile(AddressMixin, models.Model):
    """Abstract model representing a user profile.

    Attributes
    ----------
    user : django.contrib.auth.models.User
    birthday : date
    phone : str

    Properties
    ----------
    first_name : str
    last_name : str
    full_name : str
    email : str
    username : str
    """

    user = models.OneToOneField(User, verbose_name='utilisateur')
    birthday = models.DateField('date de naissance',
                                null=True, blank=True)
    phone = models.CharField('téléphone',
                             max_length=50,
                             blank=True)

    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name

    @property
    def email(self):
        return self.user.email

    @property
    def username(self):
        return self.user.username

    @property
    def full_name(self):
        return self.user.get_full_name()
    full_name.fget.short_description = 'nom complet'

    def __str__(self):
        return self.full_name

    class Meta:  # noqa
        abstract = True


class Student(Profile):
    """Model representing a student. Inherits from Profile."""

    high_school = models.ForeignKey('HighSchool',
                                    models.SET_NULL, null=True,
                                    verbose_name='lycée')
    level = models.ForeignKey('level',
                              models.SET_NULL, null=True,
                              verbose_name='niveau')
    branch = models.ForeignKey('branch',
                               models.SET_NULL, null=True,
                               verbose_name='filière')
    tutoring_group = models.ForeignKey('TutoringGroup',
                                       models.SET_NULL, null=True, blank=True,
                                       verbose_name='groupe de tutorat')

    @property
    def grade(self):
        if self.branch:
            branch_short = self.branch.short_name
        else:
            branch_short = ''
        return ' '.join(map(str, [self.level, branch_short]))
    grade.fget.short_description = 'classe'

    def get_absolute_url(self):
        return reverse('student-detail', args=[str(self.id)])

    class Meta:  # noqa
        verbose_name = 'lycéen'
        ordering = ('user__last_name', 'user__first_name')


class Tutor(Profile):
    """Model representing a tutor."""

    tutoring_group = models.ForeignKey('TutoringGroup',
                                       models.SET_NULL, null=True,
                                       verbose_name='groupe de tutorat')

    @property
    def high_school(self):
        return self.tutoring_group.high_school
    high_school.fget.short_description = 'lycée'

    def get_absolute_url(self):
        return reverse('tutor-detail', args=[str(self.id)])

    class Meta:  # noqa
        verbose_name = 'tuteur'
        ordering = ('user__last_name', 'user__first_name')


class TutoringGroup(models.Model):
    """Model representing a tutoring group."""

    high_school = models.ForeignKey('HighSchool',
                                    models.SET_NULL, null=True,
                                    verbose_name='lycée')
    level = models.ForeignKey('Level',
                              models.SET_NULL, null=True,
                              verbose_name='niveau')

    @property
    def name(self):
        return '{} ({}s)'.format(self.high_school, str(self.level).title())
    name.fget.short_description = 'nom'

    @property
    def upcoming_meetings(self):
        """Get all upcoming meetings."""
        today = datetime.date.today()
        upcoming_meetings = (self.tutoringmeeting_set
                             .filter(date__gte=today))
        return upcoming_meetings
    upcoming_meetings.fget.short_description = 'prochaines séances'

    @property
    def past_meetings(self):
        """Get all past meetings."""
        today = datetime.date.today()
        past_meetings = (self.tutoringmeeting_set
                         .order_by('-date')
                         .filter(date__lt=today))
        return past_meetings
    past_meetings.fget.short_description = 'séances passées'

    def get_absolute_url(self):
        return reverse('tutoringgroup-detail', args=[str(self.id)])

    def __str__(self):
        return self.name

    class Meta:  # noqa
        verbose_name = 'groupe de tutorat'
        verbose_name_plural = 'groupes de tutorat'
        ordering = ('high_school', 'level')


class TutoringMeeting(models.Model):
    """Model representing a tutoring meeting.

    A tutoring meeting is a temporal instance of a tutoring group, i.e.
    an event when tutors and students meet to do several activities.
    """

    date = models.DateField('date')
    high_school = models.ForeignKey('HighSchool',
                                    models.SET_NULL, null=True,
                                    verbose_name='lycée')
    tutoring_group = models.ForeignKey('TutoringGroup',
                                       models.SET_NULL, null=True,
                                       verbose_name='groupe de tutorat')

    def __str__(self):
        return self.date.strftime('%d %B %Y')

    class Meta:  # noqa
        verbose_name = 'séance de tutorat'
        verbose_name_plural = 'séances de tutorat'
        ordering = ('date',)


class HighSchool(AddressMixin, models.Model):
    """Model representing a high school."""

    name = models.CharField('nom', max_length=100, help_text='Nom du lycée')

    @property
    def tutor_set(self):
        """Return a queryset with the tutors that operate in the school."""
        return Tutor.objects.filter(tutoring_group__high_school=self)

    def get_absolute_url(self):
        return reverse('highschool-detail', args=[str(self.id)])

    def __str__(self):
        return self.name

    class Meta:  # noqa
        verbose_name = 'lycée'
        ordering = ('name',)


class Level(models.Model):
    """Model representing a class level."""

    name = models.CharField('nom', max_length=30)

    def __str__(self):
        return self.name

    class Meta:  # noqa
        verbose_name = 'niveau'
        verbose_name_plural = 'niveaux'


class Branch(models.Model):
    """Model representing a class branch."""

    name = models.CharField('nom', max_length=100)
    short_name = models.CharField('acronyme', max_length=5)

    def __str__(self):
        return self.name

    class Meta:  # noqa
        verbose_name = 'filière'
        ordering = ('name',)


class Country(models.Model):
    """Represents a country."""

    name = models.CharField('nom', max_length=50, help_text='Nom du pays')

    def __str__(self):
        return self.name

    class Meta:  # noqa
        verbose_name = 'pays'
        verbose_name_plural = 'pays'
        ordering = ('name', )
