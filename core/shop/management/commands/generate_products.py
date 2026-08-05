import random

from faker import Faker

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from accounts.models import User
from shop.models import ProductModel, ProductCategoryModel, ProductStatusType
from pathlib import Path
from django.core.files import File


BASE_DIR = Path(__file__).resolve().parent



class Command(BaseCommand):
    help = "Generate fake products"

    IMAGE_LIST = [
        "./images/img1.jpg",
        "./images/img2.jpg",
        "./images/img3.jpg",
        "./images/img4.jpg",
        "./images/img5.jpg",
        "./images/img6.jpg",
        "./images/img7.jpg",
        "./images/img8.jpg",
    ]

    def handle(self, *args, **options):
        fake = Faker(locale="fa_IR")

        users = list(User.objects.all())
        categories = list(ProductCategoryModel.objects.all())

        if not users:
            self.stdout.write(self.style.ERROR("No users found."))
            return

        if not categories:
            self.stdout.write(self.style.ERROR("No categories found."))
            return

        for _ in range(10):
            title = ' '.join([fake.word() for _ in range(1,3)])
            slug = slugify(title, allow_unicode=True)
            selected_image = random.choice(self.IMAGE_LIST)
            image_obj = File(file=open(BASE_DIR / selected_image,"rb"),name=Path(selected_image).name)

            product = ProductModel.objects.create(
                user=random.choice(users),
                title=title,
                slug=slug,
                image=image_obj,
                description=fake.paragraph(nb_sentences=10),
                brief_description=fake.paragraph(nb_sentences=1),
                stock=random.randint(0, 10),
                status=random.choice(ProductStatusType.values),
                price=random.randint(10000, 100000),
                discount_percent=random.choice([0, 5, 10, 15, 20, 25, 30, 40, 50]),
            )

            # Assign 1-3 random categories
            product.category.set(
                random.sample(
                    categories,
                    k=random.randint(1, min(3, len(categories)))
                )
            )

            self.stdout.write(
                self.style.SUCCESS(f"Created: {product.title}")
            )

        self.stdout.write(
            self.style.SUCCESS("Successfully created 10 fake products.")
        )