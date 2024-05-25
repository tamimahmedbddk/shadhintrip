import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
from SiteSetting.models import Country
from visa.models import VisaPackage, VisaType, RequiredDocuments, VisaBanner

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate the database with fake visa packages'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of visa packages to be created')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        fake = Faker()

        countries = list(Country.objects.all())

        if not countries:
            self.stdout.write(self.style.ERROR('You must have at least one country to create visa packages.'))
            return

        for _ in range(total):
            country = random.choice(countries)
            visa_type_name = fake.word().capitalize()
            visa_type, created = VisaType.objects.get_or_create(name=visa_type_name, country=country)

            title = fake.sentence(nb_words=6)
            overview = fake.paragraph(nb_sentences=3)
            description = fake.paragraph(nb_sentences=10)
            cancellation_policy = fake.paragraph(nb_sentences=2)
            visa_fee = fake.random_number(digits=2)
            processing_fee = fake.random_number(digits=2)
            our_processing_time = fake.random_int(min=1, max=30)
            visa_processing_time = fake.random_int(min=1, max=30)
            valid_for = f"{fake.random_int(min=30, max=365)} days after issued"
            number_of_entries = random.choice(['single entry', 'multiple entries'])
            max_stay = f"{fake.random_int(min=1, max=30)} days per entry"

            visa_package = VisaPackage(
                title=title,
                country=country,
                visa_type=visa_type,
                overview=overview,
                description=description,
                cancellation_policy=cancellation_policy,
                visa_fee=visa_fee,
                processing_fee=processing_fee,
                our_processing_time=our_processing_time,
                visa_processing_time=visa_processing_time,
                valid_for=valid_for,
                number_of_entries=number_of_entries,
                max_stay=max_stay,
                is_featured=fake.boolean(chance_of_getting_true=25),
                is_active=True
            )
            visa_package.save()

            # Add required documents
            for _ in range(random.randint(1, 3)):
                document_for = fake.word().capitalize()
                description = fake.paragraph(nb_sentences=2)
                required_document = RequiredDocuments(
                    visa_package=visa_package,
                    document_for=document_for,
                    description=description
                )
                required_document.save()

            self.stdout.write(self.style.SUCCESS(f'Visa Package "{title}" created'))

        self.stdout.write(self.style.SUCCESS(f'Successfully created {total} visa packages'))
