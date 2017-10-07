"""Model tests."""

import random
import datetime

from django.test import TestCase
from django.contrib.auth.models import User
from django.utils.functional import SimpleLazyObject

from internal.models import HighSchool, Student, Tutor, TutoringGroup, \
    Level, Branch, TutoringMeeting, Country, Place, Event, SingleEvent
from internal.tests.utils import GenericModelTests, id_sampler, MyTestCase


class LevelModelTest(MyTestCase):
    """Unit tests for Level model."""

    @classmethod
    def setUpTestData(self):
        self.obj = Level.objects.create(name='Première')

    def test_field_labels(self):
        self.assertFieldVerboseName(Level, 'name', 'nom')

    def test_name_max_length(self):
        self.assertMaxLength(Level, 'name', 30)

    def test_verbose_name(self):
        self.assertVerboseName(Level, 'niveau')

    def test_str(self):
        self.assertEqual('Première', str(self.obj))


class BranchModelTest(MyTestCase):
    """Unit tests for Branch model."""

    @classmethod
    def setUpTestData(self):
        self.obj = Branch.objects.create(name='Scientifique', short_name='S')

    def test_field_labels(self):
        self.assertFieldVerboseName(Branch, 'name', 'nom')

    def test_name_max_length(self):
        self.assertMaxLength(Branch, 'name', 100)

    def test_verbose_name(self):
        self.assertVerboseName(Branch, 'filière')

    def test_str(self):
        self.assertEqual('Scientifique', str(self.obj))


class CountryModelTest(MyTestCase):
    """Unit tests for Country model."""

    @classmethod
    def setUpTestData(self):
        self.obj = Country.objects.create(name='France')

    def test_field_labels(self):
        self.assertFieldVerboseName(Country, 'name', 'nom')

    def test_name_max_length(self):
        self.assertMaxLength(Country, 'name', 100)

    def test_verbose_name(self):
        self.assertVerboseName(Country, 'pays')

    def test_str(self):
        self.assertEqual('France', str(self.obj))


class StudentModelTest(MyTestCase):
    """Unit tests for Student model."""

    @classmethod
    def setUpTestData(self):
        level = Level.objects.create(name='Première')
        branch = Branch.objects.create(name='Scientifique', short_name='S')
        u = User.objects.create(first_name='Richard', last_name='Feynman')
        self.obj = Student.objects.create(user=u, level=level, branch=branch)

    def test_verbose_name(self):
        self.assertVerboseName(Student, 'lycéen')

    def test_field_labels(self):
        self.assertFieldVerboseName(Student, 'high_school', 'lycée')
        self.assertFieldVerboseName(Student, 'level', 'niveau')
        self.assertFieldVerboseName(Student, 'branch', 'filière')
        self.assertFieldVerboseName(Student, 'tutoring_group',
                                    'groupe de tutorat')
        self.assertPropertyDescription(Student, 'grade', 'classe')

    def test_grade_property(self):
        self.assertEqual(self.obj.grade, 'Première S')

    def test_tutoring_group_blank(self):
        self.assertTrue(self.get_field(Student, 'tutoring_group').blank)

    def test_get_absolute_url(self):
        return self.assertEqual(self.obj.get_absolute_url(),
                                '/internal/lyceen/1/')

    def test_str(self):
        self.assertEqual('Richard Feynman', str(self.obj))


class TutorModelTest(MyTestCase):
    """Unit tests for Tutor model."""

    @classmethod
    def setUpTestData(self):
        self.high_school = HighSchool.objects.create(name='Lycée Bidule')
        level = Level.objects.create(name='Première')
        group = TutoringGroup.objects.create(high_school=self.high_school,
                                             level=level)
        u = User.objects.create(first_name='Richard', last_name='Feynman')
        self.obj = Tutor.objects.create(user=u, tutoring_group=group)

    def test_field_labels(self):
        self.assertFieldVerboseName(Tutor, 'tutoring_group',
                                    'groupe de tutorat')
        self.assertPropertyDescription(Tutor, 'high_school', 'lycée')

    def test_high_school_property(self):
        self.assertEqual(self.obj.high_school, self.high_school)

    def test_get_absolute_url(self):
        self.assertEqual(self.obj.get_absolute_url(), '/internal/tuteur/1/')

    def test_verbose_name(self):
        self.assertVerboseName(Tutor, 'tuteur')

    def test_str(self):
        self.assertEqual('Richard Feynman', str(self.obj))


class EventTest(MyTestCase):
    """Tests for Event model."""

    def setUp(self):
        self.obj = Event(title='Test', description='Test event')

    def test_field_labels(self):
        self.assertFieldVerboseName(Event, 'title', 'titre')
        self.assertFieldVerboseName(Event, 'description', 'description')

    def test_title_max_length(self):
        self.assertMaxLength(Event, 'title', 100)

    def test_description_blank(self):
        self.assertTrue(self.get_field(Event, 'description').blank)

    def test_str(self):
        self.assertEqual('Test', str(self.obj))

    def test_is_abstract(self):
        self.assertTrue(Event._meta.abstract)


class SingleEventTest(MyTestCase):
    """Tests for SingleEvent model."""
    pass


class PlaceModelTest(MyTestCase):
    """Unit tests for Place model."""

    @classmethod
    def setUpTestData(self):
        self.obj = Place.objects.create(name='Tour Eiffel')

    def test_field_labels(self):
        self.assertFieldVerboseName(Place, 'name', 'nom')

    def test_name_max_length(self):
        self.assertMaxLength(Place, 'name', 200)

    def test_verbose_name(self):
        self.assertVerboseName(Place, 'lieu')
        self.assertVerboseNamePlural(Place, 'lieux')

    def test_str(self):
        self.assertEqual('Tour Eiffel', str(self.obj))


class HighSchoolModelTest(MyTestCase):
    """Unit tests for HighSchool model."""

    @classmethod
    def setUpTestData(self):
        self.obj = HighSchool.objects.create(id=1, name='Lycée Michelin')
        level = Level.objects.create(id=1, name='Première')
        group = TutoringGroup.objects.create(high_school=self.obj, level=level)

        def rands(s):
            return ''.join(random.choices(s, k=10))

        for _ in range(3):
            u = User.objects.create(
                username=rands('abc'),
                first_name=rands('def'),
                last_name=rands('ghi'),
            )
            Tutor.objects.create(user=u, tutoring_group=group)

    def test_field_labels(self):
        self.assertFieldVerboseName(HighSchool, 'name', 'nom')
        self.assertFieldVerboseName(HighSchool, 'rope', 'cordée')
        self.assertPropertyDescription(HighSchool, 'tutor_set', 'tuteurs')

    def test_tutor_set(self):
        expected = Tutor.objects.filter(tutoring_group__high_school=self.obj)
        self.assertQuerysetEqual(self.obj.tutor_set, map(repr, expected),
                                 ordered=False)

    def test_name_max_length(self):
        self.assertMaxLength(HighSchool, 'name', 200)

    def test_get_absolute_url(self):
        self.assertEqual(self.obj.get_absolute_url(), '/internal/lycee/1/')

    def test_verbose_name(self):
        self.assertVerboseName(HighSchool, 'lycée')

    def test_ordering_by_name(self):
        self.assertEqual(HighSchool._meta.ordering, ('name',))

    def test_str(self):
        self.assertEqual(str(self.obj), 'Lycée Michelin')


class TutoringGroupModelTest(TestCase):
    """Unit tests for TutoringGroup model."""

    @classmethod
    def setUpTestData(self):
        bidule = HighSchool.objects.create(id=1, name='Lycée Bidule')
        level = Level.objects.create(id=1, name='Première')
        group = TutoringGroup.objects.create(id=1, high_school=bidule,
                                             level=level)

        def add(cls, number, **kwargs):
            for i in range(number):
                u = User.objects.create(username=random.choices('abc', k=100))
                cls.objects.create(user=u, **kwargs)

        add(Tutor, 3, tutoring_group=group)
        add(Student, 6, tutoring_group=group)

        today = datetime.date.today()

        for i in filter(None, range(-5, 5)):
            date = today + datetime.timedelta(days=i - 5)
            TutoringMeeting.objects.create(id=i + 6, tutoring_group=group,
                                           date=date)

    gmt = GenericModelTests(TutoringGroup, sampler=id_sampler(1))

    test_high_school_label = gmt.field_verbose_name('high_school', 'lycée')

    test_level_label = gmt.field_verbose_name('level', 'niveau')

    test_name_label = gmt.property_verbose_name('name', 'nom')
    test_name_value = gmt.property_value('name', 'Lycée Bidule (Premières)')

    test_upcoming_meetings_label = gmt.property_verbose_name(
        'upcoming_meetings', 'prochaines séances')

    def test_upcoming_meetings(self):
        group = TutoringGroup.objects.get(id=1)
        upcoming = (group.tutoringmeeting_set
                    .order_by('date')
                    .filter(date__gte=datetime.date.today()))
        self.assertListEqual(list(upcoming), list(group.upcoming_meetings))

    test_past_meetings_label = gmt.property_verbose_name(
        'past_meetings', 'séances passées')

    def test_past_meetings(self):
        group = TutoringGroup.objects.get(id=1)
        today = datetime.date.today()
        past_meetings = (group.tutoringmeeting_set
                         .order_by('-date')
                         .filter(date__lt=today))
        self.assertListEqual(list(past_meetings), list(group.past_meetings))

    test_get_absolute_url = gmt.absolute_url('/internal/groupe/1/')
    test_verbose_name = gmt.verbose_name('groupe de tutorat')
    test_str = gmt.str('Lycée Bidule (Premières)')


# TODO TutoringMeetingModelTest
# TODO AddressMixinTest
# TODO ProfileModelTest
