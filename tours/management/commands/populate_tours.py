import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
from tours.models import Tour, GroupEvent, Category, Service,Country, City

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate the database with fake tours and group events'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of tours and group events to be created')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        fake = Faker()

        categories = list(Category.objects.all())
        services = list(Service.objects.all())
        users = list(User.objects.all())
        countries = list(Country.objects.all())
        cities = list(City.objects.all())

        if not categories or not services or not users or not countries or not cities:
            self.stdout.write(self.style.ERROR('You must have at least one category, service, user, country, and city to create tours and group events.'))
            return

        for _ in range(total):
            # Create Tours
            title = fake.sentence(nb_words=6)
            overview = fake.paragraph(nb_sentences=3)
            includes = fake.paragraph(nb_sentences=3)
            excludes = fake.paragraph(nb_sentences=3)
            rules = fake.paragraph(nb_sentences=2)
            refund_policy = fake.paragraph(nb_sentences=2)
            max_participants = fake.random_int(min=1, max=30)
            price = fake.random_number(digits=2)
            duration_nights = fake.random_int(min=1, max=10)
            duration_days = duration_nights + 1

            tour = Tour(
                title=title,
                overview=overview,
                includes=includes,
                excludes=excludes,
                rules=rules,
                refund_policy=refund_policy,
                max_participants=max_participants,
                price=price,
                category=random.choice(categories),
                country=random.choice(countries),
                city=random.choice(cities),
                duration_nights=duration_nights,
                duration_days=duration_days,
                is_featured=fake.boolean(chance_of_getting_true=25),
                is_active=True
            )
            tour.save()

            # Add random services to the tour
            for _ in range(random.randint(1, 3)):
                service = random.choice(services)
                tour.services.add(service)

            self.stdout.write(self.style.SUCCESS(f'Tour "{title}" created'))

            # Create Group Events
            title = fake.sentence(nb_words=6)
            overview = fake.paragraph(nb_sentences=3)
            includes = fake.paragraph(nb_sentences=3)
            excludes = fake.paragraph(nb_sentences=3)
            rules = fake.paragraph(nb_sentences=2)
            refund_policy = fake.paragraph(nb_sentences=2)
            max_participants = fake.random_int(min=1, max=30)
            price = fake.random_number(digits=2)
            duration_nights = fake.random_int(min=1, max=10)
            duration_days = duration_nights + 1
            advance_percentage = fake.random_int(min=0, max=100)
            start_date = fake.date_between(start_date='-1y', end_date='today')
            end_date = start_date + timedelta(days=duration_days)

            group_event = GroupEvent(
                title=title,
                overview=overview,
                includes=includes,
                excludes=excludes,
                rules=rules,
                refund_policy=refund_policy,
                max_participants=max_participants,
                price=price,
                category=random.choice(categories),
                country=random.choice(countries),
                city=random.choice(cities),
                duration_nights=duration_nights,
                duration_days=duration_days,
                is_featured=fake.boolean(chance_of_getting_true=25),
                is_active=True,
                booking_policy=fake.paragraph(nb_sentences=2),
                advance_percentage=advance_percentage,
                start_date=start_date,
                end_date=end_date
            )
            group_event.save()

            # Add random services to the group event
            for _ in range(random.randint(1, 3)):
                service = random.choice(services)
                group_event.services.add(service)

            self.stdout.write(self.style.SUCCESS(f'Group Event "{title}" created'))

        self.stdout.write(self.style.SUCCESS(f'Successfully created {total} tours and group events'))
