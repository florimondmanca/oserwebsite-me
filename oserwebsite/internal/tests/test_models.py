"""Model tests."""

import random
import datetime

from django.contrib.auth.models import User

from internal.models import HighSchool, Student, Tutor, TutoringGroup, \
    Level, Branch, TutoringMeeting, Country, Place, SingleEvent
from internal.tests.utils import MyTestCase


def rands(s, k=10):
    """Return a random string composed of k letters of s."""
    return ''.join(random.choices(s, k=k))


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


class SingleEventTest(MyTestCase):
    """Tests for SingleEvent model."""

    @classmethod
    def setUpTestData(self):
        today = datetime.date.today()
        now = datetime.datetime.now()
        one_hour_after = now + datetime.timedelta(hours=1)
        self.obj = SingleEvent(
            date=today,
            start=now.time(),
            end=one_hour_after.time(),
        )

    def test_is_abstract(self):
        self.assertTrue(SingleEvent._meta.abstract)

    def test_field_labels(self):
        self.assertFieldVerboseName(SingleEvent, 'date', 'date')
        self.assertFieldVerboseName(SingleEvent, 'start',
                                    'heure de début')
        self.assertFieldVerboseName(SingleEvent, 'end',
                                    'heure de fin')
        self.assertPropertyDescription(SingleEvent, 'finished',
                                       'terminé')

    def test_ordering_by_date_and_start(self):
        self.assertEqual(SingleEvent._meta.ordering, ('date', 'start'))

    def test_finished_property(self):
        end = datetime.datetime.combine(self.obj.date, self.obj.end)
        finished = datetime.datetime.today() > end
        self.assertEqual(finished, self.obj.finished)


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


class TutoringGroupModelTest(MyTestCase):
    """Unit tests for TutoringGroup model."""

    @classmethod
    def setUpTestData(self):
        self.high_school = HighSchool.objects.create(name='Lycée Michelin')
        self.level = Level.objects.create(id=1, name='Première')
        self.obj = TutoringGroup.objects.create(
            high_school=self.high_school,
            level=self.level)

        today = datetime.datetime.today()
        one_hour_after = today + datetime.timedelta(hours=1)
        start = today.time()
        end = one_hour_after.time()

        for i in filter(None, range(-5, 5)):
            date = (today + datetime.timedelta(days=i - 5)).date()
            TutoringMeeting.objects.create(
                id=i + 6, tutoring_group=self.obj,
                date=date, start=start, end=end)

    def test_field_labels(self):
        self.assertFieldVerboseName(TutoringGroup, 'high_school', 'lycée')
        self.assertFieldVerboseName(TutoringGroup, 'level', 'niveau')
        self.assertPropertyDescription(TutoringGroup, 'name', 'nom')
        self.assertPropertyDescription(TutoringGroup, 'next_meeting',
                                       'prochaine séance')
        self.assertPropertyDescription(TutoringGroup, 'upcoming_meetings',
                                       'prochaines séances')
        self.assertPropertyDescription(TutoringGroup, 'past_meetings',
                                       'séances passées')

    def test_tutor_foreign_key(self):
        self.obj.tutor_set

    def test_student_foreign_key(self):
        self.obj.student_set

    def test_tutoring_meeting_foreign_key(self):
        self.obj.tutoringmeeting_set

    def test_name_shows_high_school_and_level(self):
        self.assertEqual(self.obj.name, 'Lycée Michelin (Premières)')

    def test_upcoming_meetings(self):
        upcoming = (self.obj.tutoringmeeting_set
                    .order_by('date')
                    .filter(date__gte=datetime.date.today()))
        self.assertQuerysetEqual(upcoming,
                                 map(repr, self.obj.upcoming_meetings),
                                 ordered=False)

    def test_past_meetings(self):
        group = TutoringGroup.objects.get(id=1)
        today = datetime.date.today()
        past_meetings = (group.tutoringmeeting_set
                         .order_by('-date')
                         .filter(date__lt=today))
        self.assertQuerysetEqual(past_meetings,
                                 map(repr, self.obj.past_meetings),
                                 ordered=False)

    def test_get_absolute_url(self):
        self.assertEqual(self.obj.get_absolute_url(), '/internal/groupe/1/')

    def test_verbose_name(self):
        self.assertVerboseName(TutoringGroup, 'groupe de tutorat')
        self.assertVerboseNamePlural(TutoringGroup, 'groupes de tutorat')

    def test_ordering_by_high_school_and_level(self):
        self.assertEqual(TutoringGroup._meta.ordering,
                         ('high_school', 'level'))

    def test_str(self):
        self.assertEqual(str(self.obj), 'Lycée Michelin (Premières)')
