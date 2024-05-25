import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
from blog.models import Post, Category, Tag  # Use absolute import

# python manage.py populate_posts 100

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate the database with fake blog posts'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of posts to be created')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        fake = Faker()

        categories = Category.objects.all()
        tags = Tag.objects.all()
        users = User.objects.all()

        for _ in range(total):
            title = fake.sentence(nb_words=6)
            content = fake.paragraph(nb_sentences=10)
            category = random.choice(categories)
            author = random.choice(users)
            status = random.choice([0, 1])
            is_featured = fake.boolean(chance_of_getting_true=25)  # 25% chance to be featured
            is_active = True

            post = Post(
                title=title,
                content=content,
                category=category,
                author=author,
                status=status,
                is_featured=is_featured,
                is_active=is_active
            )
            post.save()

            # # Add random tags to the post
            # for _ in range(random.randint(1, 3)):  # Assign 1 to 3 tags
            #     tag = random.choice(tags)
            #     post.tags.add(tag)

            self.stdout.write(self.style.SUCCESS(f'Post "{title}" created'))

        self.stdout.write(self.style.SUCCESS(f'Successfully created {total} posts'))
