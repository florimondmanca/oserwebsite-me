"""Model tests."""

import random
import datetime

from django.test import TestCase
from django.contrib.auth.models import User
from django.utils.functional import SimpleLazyObject

from internal.models import HighSchool, Tutoree, Tutor, TutoringGroup, \
    Level, Branch, TutoringMeeting
from internal.tests.utils import GenericModelTests


class TutoreeModelTest(TestCase):
    """Unit tests for Tutoree model."""

    @classmethod
    def setUpTestData(self):
        level = Level.objects.create(name='Première')
        branch = Branch.objects.create(name='Scientifique', short_name='S')
        u = User.objects.create(first_name='Richard', last_name='Feynman')
        Tutoree.objects.create(id=1, user=u, level=level, branch=branch)

    GMT = GenericModelTests(Tutoree, sampler=lambda cls: cls.objects.get(id=1))

    test_high_school_label = GMT.field_verbose_name('high_school', 'lycée')

    test_level_label = GMT.field_verbose_name('level', 'niveau')

    test_branch_label = GMT.field_verbose_name('branch', 'filière')

    test_tutoring_group_label = GMT.field_verbose_name('tutoring_group',
                                                       'groupe de tutorat')

    test_grade_property_label = GMT.property_verbose_name('grade', 'classe')

    test_grade_value = GMT.property_value('grade', 'Première S')

    test_get_absolute_url = GMT.absolute_url('/internal/tutore/1/')
    test_verbose_name = GMT.verbose_name('tutoré')
    test_str = GMT.str('Richard Feynman')


class TutorModelTest(TestCase):
    """Unit tests for Tutor model."""

    @classmethod
    def setUpTestData(self):
        self.bidule = HighSchool.objects.create(name='Lycée Bidule')
        group = TutoringGroup.objects.create(name='Groupe',
                                             high_school=self.bidule)
        u = User.objects.create(first_name='Richard', last_name='Feynman')
        Tutor.objects.create(id=1, user=u, tutoring_group=group)

    GMT = GenericModelTests(Tutor, sampler=lambda cls: cls.objects.get(id=1))

    test_tutoring_group_label = GMT.field_verbose_name('tutoring_group',
                                                       'groupe de tutorat')

    test_high_school_property_label = GMT.property_verbose_name('high_school',
                                                                'lycée')

    test_high_school_value = GMT.property_value(
        'high_school', SimpleLazyObject(lambda: TutorModelTest.bidule))

    test_get_absolute_url = GMT.absolute_url('/internal/tuteur/1/')
    test_verbose_name = GMT.verbose_name('tuteur')
    test_str = GMT.str('Richard Feynman')


class HighSchoolModelTest(TestCase):
    """Unit tests for HighSchool model."""

    @classmethod
    def setUpTestData(self):
        bidule = HighSchool.objects.create(id=1, name='Lycée Bidule')
        group = TutoringGroup.objects.create(high_school=bidule)

        def add(cls, number, **kwargs):
            for i in range(number):
                u = User.objects.create(username=random.choices('abc', k=10))
                cls.objects.create(user=u, **kwargs)

        add(Tutor, 3, tutoring_group=group)
        add(Tutoree, 6, high_school=bidule)

    GMT = GenericModelTests(HighSchool,
                            sampler=lambda cls: cls.objects.get(id=1))

    test_name_label = GMT.field_verbose_name('name', 'nom')
    test_name_max_length = GMT.field_max_length('name', 100)

    test_number_tutorees = GMT.property_value('number_tutorees', 6)

    test_number_tutors = GMT.property_value('number_tutors', 3)

    test_get_absolute_url = GMT.absolute_url('/internal/lycee/1/')
    test_verbose_name = GMT.verbose_name('lycée')
    test_str = GMT.str('Lycée Bidule')


class TutoringGroupModelTest(TestCase):
    """Unit tests for TutoringGroup model."""

    @classmethod
    def setUpTestData(self):
        group = TutoringGroup.objects.create(id=1,
                                             name='Lycée Bidule (Premières)')

        def add(cls, number, **kwargs):
            for i in range(number):
                u = User.objects.create(username=random.choices('abc', k=100))
                cls.objects.create(user=u, **kwargs)

        add(Tutor, 3, tutoring_group=group)
        add(Tutoree, 6, tutoring_group=group)

        today = datetime.date.today()

        for i in filter(None, range(-5, 5)):
            date = today + datetime.timedelta(days=i - 5)
            TutoringMeeting.objects.create(id=i + 6, tutoring_group=group,
                                           date=date)

    GMT = GenericModelTests(TutoringGroup,
                            sampler=lambda cls: cls.objects.get(id=1))

    test_name_label = GMT.field_verbose_name('name', 'nom')

    test_high_school_label = GMT.field_verbose_name('high_school', 'lycée')

    test_number_tutors_label = GMT.property_verbose_name('number_tutors',
                                                         'nombre de tuteurs')
    test_number_tutors = GMT.property_value('number_tutors', 3)

    test_number_tutorees_label = GMT.property_verbose_name('number_tutorees',
                                                           'nombre de tutorés')
    test_number_tutorees = GMT.property_value('number_tutorees', 6)

    test_number_meetings_label = GMT.property_verbose_name('number_meetings',
                                                           'nombre de séances')
    test_number_meetings = GMT.property_value('number_meetings', 9)

    test_upcoming_meetings_label = GMT.property_verbose_name(
        'upcoming_meetings', 'prochaines séances')

    def test_upcoming_meetings(self):
        group = TutoringGroup.objects.get(id=1)
        upcoming = (group.tutoringmeeting_set
                    .order_by('date')
                    .filter(date__gte=datetime.date.today()))
        self.assertListEqual(list(upcoming), list(group.upcoming_meetings))

    test_past_meetings_label = GMT.property_verbose_name(
        'past_meetings', 'séances passées')

    def test_past_meetings(self):
        group = TutoringGroup.objects.get(id=1)
        today = datetime.date.today()
        past_meetings = (group.tutoringmeeting_set
                         .order_by('-date')
                         .filter(date__lt=today))
        self.assertListEqual(list(past_meetings), list(group.past_meetings))

    test_get_absolute_url = GMT.absolute_url('/internal/groupe/1/')
    test_verbose_name = GMT.verbose_name('groupe de tutorat')
    test_str = GMT.str('Lycée Bidule (Premières)')
