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
        'Ligne 1', max_length=100,
        help_text="Rue, voie, boîte postale, nom de société")
    line2 = models.CharField(
        'Ligne 2', max_length=100, blank=True,
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

    user = models.OneToOneField(User)
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


class Tutoree(Profile):
    """Model representing a tutoree. Inherits from Profile."""

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
                                       models.SET_NULL, null=True,
                                       verbose_name='groupe de tutorat')

    @property
    def grade(self):
        return '{} {}'.format(self.level, self.branch.short_name)
    grade.fget.short_description = 'classe'

    def get_absolute_url(self):
        return reverse('tutoree-detail', args=[str(self.id)])

    class Meta:  # noqa
        verbose_name = 'tutoré'


class Tutor(Profile):
    """Model representing a tutor."""

    tutoring_group = models.ForeignKey('TutoringGroup',
                                       models.SET_NULL, null=True,
                                       verbose_name='groupe de tutorat')

    @property
    def high_school(self):
        return self.tutoring_group.high_school

    def get_absolute_url(self):
        return reverse('tutor-detail', args=[str(self.id)])

    class Meta:  # noqa
        verbose_name = 'tuteur'


class TutoringGroup(models.Model):
    """Model representing a tutoring group."""

    name = models.CharField('nom', max_length=100)
    high_school = models.ForeignKey('HighSchool',
                                    models.SET_NULL, null=True,
                                    verbose_name='lycée')

    @property
    def number_tutors(self):
        """Number of tutors in this group."""
        return self.tutor_set.count()
    number_tutors.fget.short_description = 'Nombre de tuteurs'

    @property
    def number_tutorees(self):
        """Number of tutorees in this group."""
        return self.tutoree_set.count()
    number_tutorees.fget.short_description = 'Nombre de tutorés'

    @property
    def number_meetings(self):
        """Number of meetings for this group."""
        return self.tutoringmeeting_set.count()
    number_meetings.fget.short_description = 'Nombre de séances'

    def upcoming_meetings_first(self, first=5):
        """Get a list of the next upcoming meetings i.e. those after today).

        Parameters
        ----------
        first : int, optional
            The number of upcoming meetings to get (default is 5).
            Pass None to get all upcoming meetings.
        """
        today = datetime.date.today()
        upcoming_meetings = (self.tutoringmeeting_set
                             .order_by('date')
                             .filter(date__gte=today))
        return upcoming_meetings[:first]

    def upcoming_meetings(self):
        """Get all upcoming meetings."""
        return self.upcoming_meetings_first(None)

    def past_meetings_first(self, first=5):
        """Get a list of the the past meetings (i.e. those before today).

        Parameters
        first : int, optional
            The number of past meetings to get (default is 5).
            Pass None to get all past meetings.
        """
        today = datetime.date.today()
        past_meetings = (self.tutoringmeeting_set
                         .order_by('-date')
                         .filter(date__lt=today))
        return past_meetings[:first]

    def past_meetings(self):
        """Get all past meetings."""
        return self.past_meetings_first(None)

    def get_absolute_url(self):
        return reverse('tutoringgroup-detail', args=[str(self.id)])

    def __str__(self):
        return self.name

    class Meta:  # noqa
        verbose_name = 'groupe de tutorat'
        verbose_name_plural = 'groupes de tutorat'


class TutoringMeeting(models.Model):
    """Model representing a tutoring meeting.

    A tutoring meeting is a temporal instance of a tutoring group, i.e.
    an event when tutors and tutorees meet to do several activities.
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


class HighSchool(AddressMixin, models.Model):
    """Model representing a high school."""

    name = models.CharField('nom', max_length=100, help_text='Nom du lycée')

    @property
    def number_tutorees(self):
        """Count how many tutorees are in the school."""
        return self.tutoree_set.count()

    @property
    def number_tutors(self):
        """Count how many tutors operte in the school."""
        tutors = Tutor.objects.filter(tutoring_group__high_school=self)
        return tutors.count()

    def get_absolute_url(self):
        return reverse('highschool-detail', args=[str(self.id)])

    def __str__(self):
        return self.name

    class Meta:  # noqa
        verbose_name = 'lycée'


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


class Country(models.Model):
    """Represents a country."""

    name = models.CharField('nom', max_length=50, help_text='Nom du pays')

    def __str__(self):
        return self.name

    class Meta:  # noqa
        verbose_name = 'pays'
        verbose_name_plural = 'pays'
