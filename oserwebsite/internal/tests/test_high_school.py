import random

from django.test import TestCase
from django.contrib.auth.models import User

from internal.models import HighSchool, Tutoree, Tutor, TutoringGroup


class HighSchoolModelTest(TestCase):

    @classmethod
    def setUpTestData(self):
        bidule = HighSchool.objects.create(name='Lycée Bidule')
        group = TutoringGroup.objects.create(high_school=bidule)

        def add_tutoree(number):
            for i in range(number):
                u = User.objects.create(username=random.choices('abc', k=10))
                Tutoree.objects.create(user=u, high_school=bidule)

        def add_tutor(number):
            for i in range(number):
                u = User.objects.create(username=random.choices('abc', k=10))
                Tutor.objects.create(user=u, tutoring_group=group)

        add_tutor(3)
        add_tutoree(6)

    def test_name_label(self):
        high_school = HighSchool.objects.get(id=1)
        label = high_school._meta.get_field('name').verbose_name
        self.assertEqual('nom', label)

    def test_name_max_length(self):
        high_school = HighSchool.objects.get(id=1)
        max_length = high_school._meta.get_field('name').max_length
        self.assertEqual(100, max_length)

    def test_get_absolute_url(self):
        high_school = HighSchool.objects.get(id=1)
        self.assertEqual('/internal/lycee/1/', high_school.get_absolute_url())

    def test_number_of_tutorees(self):
        high_school = HighSchool.objects.get(id=1)
        self.assertEqual(6, high_school.number_tutorees)

    def test_number_of_tutors(self):
        high_school = HighSchool.objects.get(id=1)
        self.assertEqual(3, high_school.number_tutors)

    def test_str_is_name(self):
        high_school = HighSchool.objects.get(id=1)
        self.assertEqual('Lycée Bidule', str(high_school))
