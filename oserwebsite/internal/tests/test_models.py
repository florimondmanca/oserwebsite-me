"""Model tests."""

import random
import datetime

from django.test import TestCase
from django.contrib.auth.models import User
from django.utils.functional import SimpleLazyObject
from django.core.exceptions import FieldDoesNotExist

from internal.models import HighSchool, Student, Tutor, TutoringGroup, \
    Level, Branch, TutoringMeeting, Country, Place
from internal.tests.utils import GenericModelTests, id_sampler


class MyTestCase(TestCase):
    """Extends Django's test case with extra assert methods."""

    def _get_field(self, obj, field_name):
        """Get a model's field object by name."""
        return obj._meta.get_field(field_name)

    def assertVerboseName(self, model, expected):
        """Compare a model's verbose_name meta attribute to an expected value.

        Parameters
        ---------
        model : models.Model
        expected : str
        """
        name = model._meta.verbose_name
        self.assertEqual(name, expected)

    def assertFieldVerboseName(self, obj, field_name, expected):
        """Compare an object's field verbose_name to an expected value.

        Parameters
        ---------
        obj : models.Model instance
            An instance of a model.
        field_name : str
        expected : str
        """
        name = self._get_field(obj, field_name).verbose_name
        self.assertEqual(name, expected)

    def assertPropertyDescription(self, obj, prop_name, expected):
        """Compare an object's property short_description to an expected value.

        Parameters
        ---------
        obj : models.Model instance
            An instance of a model.
        prop_name : str
        expected : str
        """
        prop = type(obj).__dict__[prop_name]
        name = prop.fget.short_description
        self.assertEqual(name, expected)

    def assertMaxLength(self, obj, field_name, expected):
        """Compare an object's field max_length to an expected value.

        Typically used on CharFields.

        Parameters
        ---------
        obj : models.Model instance
            An instance of a model.
        field_name : str
            The corresponding field must have a max_length attribute.
        expected : int
        """
        length = self._get_field(obj, field_name).max_length
        self.assertEqual(length, expected)


class LevelModelTest(MyTestCase):
    """Unit tests for Level model."""

    @classmethod
    def setUpTestData(self):
        self.obj = Level.objects.create(name='Première')

    def test_name_label(self):
        self.assertFieldVerboseName(self.obj, 'name', 'nom')

    def test_name_max_length(self):
        self.assertMaxLength(self.obj, 'name', 30)

    def test_verbose_name(self):
        self.assertVerboseName(Level, 'niveau')

    def test_str(self):
        self.assertEqual('Première', str(self.obj))


class BranchModelTest(MyTestCase):
    """Unit tests for Branch model."""

    @classmethod
    def setUpTestData(self):
        self.obj = Branch.objects.create(name='Scientifique', short_name='S')

    def test_name_label(self):
        self.assertFieldVerboseName(self.obj, 'name', 'nom')

    def test_name_max_length(self):
        self.assertMaxLength(self.obj, 'name', 100)

    def test_verbose_name(self):
        self.assertVerboseName(Branch, 'filière')

    def test_str(self):
        self.assertEqual('Scientifique', str(self.obj))


class CountryModelTest(MyTestCase):
    """Unit tests for Country model."""

    @classmethod
    def setUpTestData(self):
        self.obj = Country.objects.create(name='France')

    def test_name_label(self):
        self.assertFieldVerboseName(self.obj, 'name', 'nom')

    def test_name_max_length(self):
        self.assertMaxLength(self.obj, 'name', 100)

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
        self.assertFieldVerboseName(self.obj, 'high_school', 'lycée')
        self.assertFieldVerboseName(self.obj, 'level', 'niveau')
        self.assertFieldVerboseName(self.obj, 'branch', 'filière')
        self.assertFieldVerboseName(self.obj, 'tutoring_group',
                                    'groupe de tutorat')
        self.assertPropertyDescription(self.obj, 'grade', 'classe')

    def test_grade_property(self):
        self.assertEqual(self.obj.grade, 'Première S')

    def test_get_absolute_url(self):
        return self.assertEqual(self.obj.get_absolute_url(),
                                '/internal/lyceen/1/')

    def test_str(self):
        self.assertEqual('Richard Feynman', str(self.obj))


class TutorModelTest(TestCase):
    """Unit tests for Tutor model."""

    @classmethod
    def setUpTestData(self):
        self.bidule = HighSchool.objects.create(name='Lycée Bidule')
        level = Level.objects.create(name='Première')
        group = TutoringGroup.objects.create(high_school=self.bidule,
                                             level=level)
        u = User.objects.create(first_name='Richard', last_name='Feynman')
        Tutor.objects.create(id=1, user=u, tutoring_group=group)

    gmt = GenericModelTests(Tutor, sampler=id_sampler(1))

    test_tutoring_group_label = gmt.field_verbose_name('tutoring_group',
                                                       'groupe de tutorat')

    test_high_school_property_label = gmt.property_verbose_name('high_school',
                                                                'lycée')

    test_high_school_value = gmt.property_value(
        'high_school', SimpleLazyObject(lambda: TutorModelTest.bidule))

    test_get_absolute_url = gmt.absolute_url('/internal/tuteur/1/')
    test_verbose_name = gmt.verbose_name('tuteur')
    test_str = gmt.str('Richard Feynman')


class PlaceModelTest(TestCase):
    """Unit tests for Place model."""

    @classmethod
    def setUpTestData(self):
        Place.objects.create(id=1, name='Tour Eiffel')

    gmt = GenericModelTests(Place, sampler=id_sampler(1))

    test_name_label = gmt.field_verbose_name('name', 'nom')
    test_name_max_length = gmt.field_max_length('name', 200)

    test_verbose_name = gmt.verbose_name('lieu')
    test_str = gmt.str('Tour Eiffel')


class HighSchoolModelTest(TestCase):
    """Unit tests for HighSchool model."""

    @classmethod
    def setUpTestData(self):
        bidule = HighSchool.objects.create(id=1, name='Lycée Bidule')
        level = Level.objects.create(id=1, name='Première')
        group = TutoringGroup.objects.create(high_school=bidule, level=level)

        def add(cls, number, **kwargs):
            for i in range(number):
                u = User.objects.create(username=random.choices('abc', k=10))
                cls.objects.create(user=u, **kwargs)

        add(Tutor, 3, tutoring_group=group)
        add(Student, 6, high_school=bidule)

    gmt = GenericModelTests(HighSchool, sampler=id_sampler(1))

    test_name_label = gmt.field_verbose_name('name', 'nom')
    test_name_max_length = gmt.field_max_length('name', 200)

    test_get_absolute_url = gmt.absolute_url('/internal/lycee/1/')
    test_verbose_name = gmt.verbose_name('lycée')
    test_str = gmt.str('Lycée Bidule')


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
