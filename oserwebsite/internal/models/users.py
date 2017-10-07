"""Users of the internal website."""

from django.db import models
from django.urls import reverse
from . import base


class Student(base.Profile):
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


class Tutor(base.Profile):
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
