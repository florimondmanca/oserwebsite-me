"""Models are defined here."""

import datetime

from django.db import models


class Event(models.Model):
    """Represents an event.

    Fields
    ------
    title : models.CharField
        Title of the event.
    description : models.TextField
        Short description of the event, optional.
    start : models.DateTimeField
        Start date and time of the event.
    end : models.DateTimeField
        End date and time of the event.
    """

    title = models.CharField('titre', max_length=100)
    description = models.TextField('description', blank=True)

    def __str__(self):
        return self.title

    class Meta:  # noqa
        abstract = True


class SingleEvent(Event):
    """Repreents an event that occurs on a specific day.

    Fields
    ------
    title : models.CharField
        Title of the event.
    description : models.TextField
        Short description of the event, optional.
    date : models.DateField
        Date of the event.
    start : models.TimeField
        Start time of the event.
    end : models.TimeField
        End time of the event.
    """

    date = models.DateField()
    start = models.TimeField('heure de début')
    end = models.TimeField('heure de fin')

    @property
    def finished(self):
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
