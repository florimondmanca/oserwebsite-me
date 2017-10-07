"""Models related to tutoring activities.

Models defined here:
- HighSchool
- TutoringGroup
- TutoringMeeting
- Rope
"""

import datetime

from django.db import models
from django.shortcuts import reverse
from django.utils.formats import date_format

from . import base
from .users import Tutor


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


class HighSchool(base.Place):
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
