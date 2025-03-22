# TODO: Keep Practicing!
# - [X] ManyToOne + Recursive
# - [X] ManyToMany with and without through and through_fields dict
# - [X] objects.create in Intermediate, add, set, create, clear using Relationship
# - [X] Practice Queries accessing all three involved tables by their name or a name defined by related_query_field. Also practice access from shell using related_name this time.
# - [X] In custom intermediate tables practice with and without setting the uniqueness through Meta, unique_together, or preferably with unique constraints.
# - [X] Get very clear on what is happening in database table and what is created or deleted in response.
# - [X] When done, move on to another session of consumption.

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date
import random
from faker import Faker
from misc.helper_functions import reset_sqlite_sequences


class Author(models.Model):
    name = models.CharField(max_length=30)
    books = models.ManyToManyField("Book", through="AuthorBooksThrough")

    @classmethod
    def instance_generator(cls, n=100):
        return_list = []
        for _ in range(n):
            faker_name = Faker().name()

            generated_instance = cls(
                name=faker_name,
            )
            generated_instance.save()
            return_list.append(generated_instance)
        return return_list

    @classmethod
    def db_reset(cls):
        print("deleted ->", cls.objects.all().delete())
        reset_sqlite_sequences(
            tablename=cls.__name__.lower(), app_name="app_two"
        )


class Book(models.Model):
    title = models.CharField(max_length=60)
    edition = models.SmallIntegerField()
    year = models.IntegerField(
        validators=[
            min_year := MinValueValidator(1000),
            max_year := MaxValueValidator(date.today().year),
        ]
    )

    @classmethod
    def instance_generator(cls, n=100):
        return_list = []
        for _ in range(n):
            faker_title = Faker().sentence()
            rand_edition = random.randint(1, 10)
            rand_year = random.randint(
                cls.min_year.limit_value, cls.max_year.limit_value
            )
            # rand_author = random.choice(Author.objects.all())
            generated_instance = cls(
                title=faker_title,
                edition=rand_edition,
                year=rand_year,
                # author=rand_author,
            )
            generated_instance.save()
            return_list.append(generated_instance)
        return return_list

    @classmethod
    def db_reset(cls):
        print("deleted ->", cls.objects.all().delete())
        reset_sqlite_sequences(
            tablename=cls.__name__.lower(), app_name="app_two"
        )


class AuthorBooksThrough(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    whatever_through_field = models.IntegerField()

    class Meta:
        unique_together = ["author", "book"]

    @classmethod
    def instance_generator(cls, authors, books, n=None):
        if n is None:
            n = max(len(authors), len(books))
        return_list = []
        for _ in range(n):
            rand_author = random.choice(authors)
            rand_book = random.choice(books)
            rand_whatever_through_field = random.randint(1, 1000)

            # rand_author = random.choice(Author.objects.all())
            generated_instance = cls(
                author=rand_author,
                book=rand_book,
                whatever_through_field=rand_whatever_through_field,
                # author=rand_author,
            )
            return_list.append(generated_instance)
        cls.objects.bulk_create(return_list, ignore_conflicts=True)

        return return_list

    @classmethod
    def db_reset(cls):
        print("deleted ->", cls.objects.all().delete())
        reset_sqlite_sequences(
            tablename=cls.__name__.lower(), app_name="app_two"
        )


#### Faker Reference ####
"""
1. Personal Information:
Name: fake.name(), fake.first_name(), fake.last_name()
Address: fake.address(), fake.city(), fake.state(), fake.zipcode()
Email: fake.email()
Phone Number: fake.phone_number()
Username: fake.user_name()
Date of Birth: fake.date_of_birth()
Job: fake.job()
SSN (Social Security Number): fake.ssn()
2. Text and Paragraphs:
Sentence: fake.sentence()
Paragraph: fake.paragraph()
Text: fake.text()
Lorem Ipsum Text: fake.lorem_paragraph()
3. Dates and Times:
Date: fake.date()
Time: fake.time()
DateTime: fake.date_time(), fake.date_time_this_year()
Past and Future Dates: fake.date_this_month(), fake.date_this_decade()
4. Financial Information:
Credit Card: fake.credit_card_number(), fake.credit_card_expire()
Currency: fake.currency()
Price: fake.price()
5. Company/Business Information:
Company Name: fake.company()
Company Suffix: fake.company_suffix()
Catch Phrase: fake.catch_phrase()
BS (Business Slogan): fake.bs()
6. Geographic Information:
Country: fake.country()
Country Code: fake.country_code()
Latitude and Longitude: fake.latitude(), fake.longitude()
Coordinates: fake.local_latlng()
7. Internet-Related:
URL: fake.url()
Domain Name: fake.domain_name()
IP Address: fake.ipv4(), fake.ipv6()
User Agent: fake.user_agent()
8. Images:
Image URL: fake.image_url()
9. Miscellaneous:
Boolean: fake.boolean()
Color: fake.color_name(), fake.hex_color()
Random Word: fake.word()
UUID (Universally Unique Identifier): fake.uuid4()
"""
