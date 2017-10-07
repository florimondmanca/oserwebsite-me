"""Base (abstract) models for internal."""

from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
import datetime
from django.shortcuts import reverse
from django.utils.formats import date_format


class AddressMixin(models.Model):
    """Mixin that adds address-related fields to a Model.

    Fields
    ------
    line1 : char[100]
        First line of the address.
    line2 : char[100][blank]
        Second line of the address, not mendatory.
    post_code : char[20]
    city : char[50]
    country : FK[Country]

    Properties
    ----------
    address : str
        A multiline string displaying the full address:
            <line1>
            <line2>
            <postcode> <city>
            <country>
    address_inline : str
        A string displaying the full address, made to be used inline:
            <line1>, <line2>, <postcode> <city>, <country>
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

    def _formatted_address(self, sep=', '):
        """Return a single-string formatted version of the address.

        The fields line1, line2, post_code, city and country are displayed
        in a sequence, separated by the specified sep string.

        Parameters
        ----------
        sep : str, optional
            Separator used to display the address.

        Example
        -------
        >>> a._formatted_address(sep=', ')
        3 rue Jean Maillard, Appt 140, 45600 Valence, France
        """
        city_line = '{} {}'.format(self.post_code, self.city.upper())
        _lines = (self.line1, self.line2, city_line,
                  self.country.name.upper())
        lines = [line for line in _lines if line]
        return mark_safe(sep.join(lines))

    @property
    def address_inline(self):
        return self._formatted_address(sep=', ')

    @property
    def address(self):
        return self._formatted_address(sep='<br/>')

    class Meta:  # noqa
        abstract = True


class Place(AddressMixin):
    """Represents a place that has a name and an address.

    Fields
    ------
    name : char[200]
    @include fields from AddressMixin
    """

    name = models.CharField('nom', max_length=200)

    def __str__(self):
        return self.name

    class Meta:  # noqa
        verbose_name = 'lieu'
        verbose_name_plural = 'lieux'
        ordering = ('name',)


class Profile(AddressMixin):
    """Abstract model representing a user profile.

    A user profile has a related django User, an address, a birthday and
    a phone.

    Fields
    ----------
    user : django.contrib.auth.models.User
    birthday : date[blank]
    phone : char[50][blank]

    Properties
    ----------
    first_name : str
        The django User's first name field.
    last_name : str
        The django User's last name field.
    full_name : str
        First name and last name, e.g. 'John Smith'.
    email : str
        The django User's email field.
    username : str
        The django User's username field.
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


class Country(models.Model):
    """Represents a country."""

    name = models.CharField('nom', max_length=100)

    def __str__(self):
        return self.name

    class Meta:  # noqa
        verbose_name = 'pays'
        verbose_name_plural = 'pays'
        ordering = ('name', )


class Event(models.Model):
    """Abstract model for representing an event.

    Fields
    ------
    title : models.CharField
        Title of the event.
    description : models.TextField
        Short description of the event, optional.
    """

    title = models.CharField('titre', max_length=100)
    description = models.TextField('description', blank=True)

    def __str__(self):
        return self.title

    class Meta:  # noqa
        abstract = True


class SingleEventManager(models.Manager):
    """Custom manager for SingleEvent model.

    Methods
    -------
    finished() -> queryset of finished events
    incoming() -> queryset of incoming events
    """

    def finished(self):
        """Return finished events only."""
        today = datetime.date.today()
        return self.filter(date__lt=today)

    def incoming(self):
        """Return incoming events only."""
        today = datetime.date.today()
        return self.filter(date__gte=today)


class SingleEvent(Event):
    """Repreents an event that occurs on a specific day.

    Fields
    ------
    @include fields from Event
    date : models.DateField
        Date of the event.
    start : models.TimeField
        Start time of the event.
    end : models.TimeField
        End time of the event.

    Properties
    ----------
    finished : bool
        True if the event is finished, i.e. its datetime is in the past.
    """

    date = models.DateField()
    start = models.TimeField('heure de début')
    end = models.TimeField('heure de fin')

    objects = SingleEventManager()

    @property
    def finished(self):
        """True if the event's datetime is strictly in the past."""
        end = datetime.datetime.combine(self.date, self.end)
        return end < datetime.datetime.today()

    class Meta:  # noqa
        ordering = ('date', 'start',)
        abstract = True


class Visit(SingleEvent):
    """Represents a visit event to which students can participate."""

    place = models.ForeignKey('Place', models.SET_NULL, null=True,
                              verbose_name='lieu')
    students = models.ManyToManyField('Student')

    class Meta:  # noqa
        ordering = SingleEvent._meta.ordering
        verbose_name = 'sortie'


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
    def next_meeting(self):
        """Get next meeting."""
        return self.upcoming_meetings.first()
    next_meeting.fget.short_description = 'prochaine séance'

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
    tutoring_group = models.ForeignKey('TutoringGroup',
                                       models.SET_NULL, null=True,
                                       verbose_name='groupe de tutorat')

    @property
    def high_school(self):
        return self.tutoring_group.high_school
    high_school.fget.short_description = 'lycée'

    def __str__(self):
        return date_format(self.date, 'DATE_FORMAT')

    class Meta:  # noqa
        verbose_name = 'séance de tutorat'
        verbose_name_plural = 'séances de tutorat'
        ordering = ('date', 'tutoring_group',)


class HighSchool(Place):
    """Model representing a high school."""

    rope = models.ForeignKey('Rope', models.SET_NULL, null=True,
                             verbose_name='cordée')

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


class Rope(models.Model):
    """Model representing a rope, i.e. a group of high schools.

    French equivalent name : Cordée de la Réussite
    See: http://www.cordeesdelareussite.fr
    """

    name = models.CharField('nom', max_length=100)

    def __str__(self):
        return self.name

    class Meta:  # noqa
        verbose_name = 'cordée'
        ordering = ('name',)


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


class Student(Profile):
    """Model representing a student. Inherits from Profile."""

    high_school = models.ForeignKey('HighSchool',
                                    models.SET_NULL, null=True,
                                    verbose_name='lycée')
    level = models.ForeignKey('Level',
                              models.SET_NULL, null=True,
                              verbose_name='niveau')
    branch = models.ForeignKey('Branch',
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
        ordering = ('user__last_name', 'user__first_name',
                    'high_school', 'level')


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
