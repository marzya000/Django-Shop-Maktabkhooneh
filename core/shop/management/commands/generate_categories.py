from faker import Faker

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from shop.models import ProductCategoryModel


class Command(BaseCommand):
    help = "Generate fake categories"

    def handle(self, *args, **options):
        fake = Faker()

        created = 0

        while created < 10:
            title = fake.unique.word().title()
            slug = slugify(title, allow_unicode=True)
            
            ProductCategoryModel.objects.get_or_create(title=title,slug=slug)

            created += 1
            self.stdout.write(
                self.style.SUCCESS(f"Created: {title}")
            )

        self.stdout.write(
            self.style.SUCCESS("Successfully created 10 fake categories.")
        )
