"""resetdb command."""

import random
import datetime

from django.core.management.base import BaseCommand
from django.core.management import call_command

from django.contrib.auth.models import User
from internal.models import Tutor, Student, TutoringGroup, TutoringMeeting, \
    HighSchool, Level, Branch, Country


class Command(BaseCommand):
    """Erase the database and initialize it with dummy data."""

    def handle(self, *args, **options):
        confirm_msg = """\
This command will erase the database (including superusers) and
replace its contents with pre-defined ones. Continue? (y/n) """
        confirm = input(self.style.WARNING(confirm_msg))
        if confirm != 'y':
            self.stdout.write('Aborting...')
            return

        call_command('flush')
        self.stdout.write(self.style.NOTICE('Please create a new super user:'))
        call_command('createsuperuser')
        superuser = User.objects.filter(is_superuser=True).first()
        superuser.first_name = input('Superuser first name: ') or ''
        superuser.last_name = input('Superuser last name: ') or ''
        superuser.save()
        self.stdout.write('Successfully set superuser first and last name.')

        usernames = [
            'overlookedtrophy',
            'orioletravel',
            'barsswimmer',
            'coaticoloured',
            'draggingnoodle',
            'peevishoperand',
            'coigachslanders',
            'pizzlecaribou',
            'languagesoloman',
            'milksopdouble',
            'analogylaptops',
            'antigravitypub',
            'thingavel',
            'horatiopioneering',
            'rearendanger',
            'cropleyhumidity',
            'chimpritzy',
            'cultivatedcitrine',
            'toshmild',
            'afocalcompounds',
            'respectreverse',
            'incubateperl',
            'swinhoehill',
            'daddyremove',
            'camelpickled'
        ]
        for i in range(40):
            usernames.append(
                random.choice(usernames)[:10] + random.choice(usernames)[:10])
        usernames = set(usernames)

        first_names = (
            'Jean', 'Marie', 'Michel', 'Alexandre', 'Martin',
            'Bernard', 'Axel', 'Florence', 'Isabelle', 'Marc',
            'Donald', 'Harry', 'Harold', 'Justin', 'Julien', 'Jacques',
        )

        last_names = (
            'Dupont', 'Laporte', 'Micheaux', 'Durand', 'Clavier',
            'Gavin', 'Lehoucq', 'Kobo', 'Baratte', 'Shi', 'Ly', 'Manca',
            'Williams', 'Urtanga', 'Oloupio', 'Loquancourt', 'Malle',
        )

        lines1 = (
            '1 rue Gustave Eiffel', '67 rue Clement Marot', '42 rue Cazade',
            '73 Rue du Palais', '9 rue du Paillle en queue',
            '55 Place de la Madeleine', '99 rue La Boétie',
            '45 Faubourg Saint Honoré', '72 Square de la Couronne',
            '23 Place de la Fontaine',
        )

        cities = (
            'Châtenay-Malabry', 'Montreuil', 'Paris', 'Antony', 'Clamart',
            'Sceaux', 'Massy', 'Palaiseau', 'Gif-sur-Yvette', 'Vélizy',
            'Fresnes', 'Bourg-la-Reine', 'Cachan', 'Wissous', 'Thiais',
        )

        post_codes = (
            '34053', '78865', '55000', '34556', '67873', '12331', '40694',
            '92290', '45600', '74003', '93100', '34566', '10220', '30450',
        )

        high_school_names = (
            'Lycée Saint-Jules', 'Lycée Jean Bernard', 'Lycée Jean Jaurès',
            'Lycée Hervé Biausser', 'Lycée Henri Micheaux', 'Lycée Magnart',
            'Lycée Henri Wallon', 'Lycée des Apprentis', 'Lycée Michel Fabre',
            'Lycée Robert Peugeot', 'Lycée Berlioz', 'Lycée Hugues Martin',
        )

        # create countries
        Country.objects.create(name='France').save()
        self.stdout.write('Created 1 country: France')

        countries = (
            Country.objects.get(name='France'),
        )

        def random_address():
            return {
                'line1': random.choice(lines1),
                'post_code': random.choice(post_codes),
                'city': random.choice(cities),
                'country': random.choice(countries),
            }

        # create levels
        Level.objects.create(name='Seconde').save()
        Level.objects.create(name='Première').save()
        Level.objects.create(name='Terminale').save()
        self.stdout.write('Created 3 levels: Seconde, Première, Terminale')

        # create branches
        Branch.objects.create(name='Scientifique', short_name='S').save()
        Branch.objects.create(name='Littéraire', short_name='L').save()
        Branch.objects.create(
            name="Economique et Social", short_name='ES').save()
        Branch.objects.create(name="Professionnelle", short_name="Pro").save()
        self.stdout.write('Created 4 branches: S, L, ES, Pro')

        # create high schools
        for name in high_school_names:
            high_school = HighSchool.objects.create(
                name=name,
                **random_address(),
            )
            high_school.save()

        self.stdout.write('Create {} high schools'
                          .format(len(high_school_names)))

        # create tutoring groups
        n_groups = 10
        for i in range(n_groups):
            high_school = random.choice(HighSchool.objects.all())
            level = random.choice(Level.objects.all())
            group = TutoringGroup.objects.create(high_school=high_school,
                                                 level=level)
            group.save()
        self.stdout.write('Created {} tutoring groups'.format(n_groups))

        # create users
        n_tutors = 0
        n_students = 0
        for username in usernames:
            u = User.objects.create_user(
                username=username,
                first_name=random.choice(first_names),
                last_name=random.choice(last_names),
                password='onions')
            u.save()

            status = random.choice(('tutor', 'student', 'student'))
            if status == 'tutor':
                tutor = Tutor.objects.create(
                    user=u,
                    **random_address(),
                    tutoring_group=random.choice(TutoringGroup.objects.all()),
                )
                tutor.save()
                n_tutors += 1
            elif status == 'student':
                student = Student.objects.create(
                    user=u,
                    **random_address(),
                    high_school=random.choice(HighSchool.objects.all()),
                    level=random.choice(Level.objects.all()),
                    branch=random.choice(Branch.objects.all()),
                    tutoring_group=random.choice(TutoringGroup.objects.all()),
                )
                student.save()
                n_students += 1
        self.stdout.write('Created {} users ({} students and {} tutors)'
                          .format(len(usernames), n_students, n_tutors))

        # create a student called Bernard
        bernard = User.objects.create(username='bernard',
                                      first_name='Bernard',
                                      last_name='Bernard',
                                      password='onions')
        Student.objects.create(
            user=bernard,
            **random_address(),
            tutoring_group=random.choice(TutoringGroup.objects.all()))
        self.stdout.write('Created student bernard')

        # assign superuser as tutor
        Tutor.objects.create(
            user=superuser,
            **random_address(),
            tutoring_group=random.choice(TutoringGroup.objects.all())
        )
        self.stdout.write('Superuser you created was made a tutor')

        # create tutoring meetings
        def random_date():
            start = datetime.date.today()
            delta_days = random.randrange(100)
            date = start + datetime.timedelta(days=delta_days)
            return date

        n_meetings = 20
        for i in range(n_meetings):
            meeting = TutoringMeeting.objects.create(
                date=random_date(),
                high_school=random.choice(HighSchool.objects.all()),
                tutoring_group=random.choice(TutoringGroup.objects.all()),
            )
            meeting.save()
        self.stdout.write('Created {} tutoring meetings'.format(n_meetings))

        self.stdout.write(self.style.SUCCESS('Database reset!'))
