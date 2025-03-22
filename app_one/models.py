import os
from multiprocessing import Pool
from django.db import models
from faker import Faker
import random
from scripts.fetch_top_players import fetch_top_100_players
from misc.helper_functions import reset_sqlite_sequences

"""
Instead of using multiple model files and actually making the whole thing even more complicated, go for different apps whenever you need to. The reason for this is the fact that creating a new file is still prone to database table name conflicts because the table name in the database has an app-based prefix and not a model-file-based prefix. You would have to keep checking your other model files for existing table names.
With different apps there is no such issue as you can essentially start from scratch with a new app even though the database is not completely empty. In addition, using an existing name in the current file is a lot easier to detect, but keep in mind that a warning is not raised by vscode.
"""


class Person(models.Model):

    sport_choices = [
        ("tennis", "Tennis"),
        ("soccer", "Soccer"),
        ("basketball", "Basketball"),
    ]

    ### Model fields ###
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=200)
    has_kids = models.BooleanField("do you have kids?", default=False)
    is_married = models.BooleanField("are you married?", default=False)
    dob = models.DateField("date of birth")

    # No need for verbose name as Django will auto replace the '_' with a space
    id_number = models.IntegerField(unique=True)
    favorite_player = models.CharField(max_length=30)
    favorite_sport = models.CharField(
        max_length=30,
        choices=sport_choices,
    )

    ### Class methods ###
    @classmethod
    def db_reset(cls):
        print("deleted ->", cls.objects.all().delete())
        reset_sqlite_sequences(
            tablename=cls.__name__.lower(), app_name="app_one"
        )

    @classmethod
    def parallel_instance_generator(cls, n=1000):
        """
        took 90 secs to generate 1,000,000 instances on 16-core 5700X3D and 10 secs to bulk insert them.
        """
        NUM_PROCESSES = os.cpu_count()
        batch_size = n // NUM_PROCESSES

        with Pool(processes=NUM_PROCESSES) as pool:
            all_batches = pool.map(
                cls._instance_generator, [batch_size] * NUM_PROCESSES
            )

        full_list = [obj for batch in all_batches for obj in batch]
        cls.objects.bulk_create(full_list, ignore_conflicts=True)
        return full_list

    @classmethod
    def _instance_generator(cls, n: int):
        """
        calls _generate_one_person n times, and returns a list.
        """
        persons = [cls._generate_one_person() for _ in range(n)]
        # for _ in range(n):
        #     persons.append(cls._generate_one_person())
        return persons

    @classmethod
    def _generate_one_person(cls):
        """
        generates an returns an instance of the person model.
        """
        # creating an instance of Faker to be used as a random Field generator
        faker = Faker()

        fake_name = f"{faker.first_name()} {faker.last_name()}"
        fake_description = faker.paragraph()
        rand_has_kids = random.choice((True, False))
        rand_is_married = random.choice((True, False))
        fake_dob = faker.date_of_birth(minimum_age=18)
        rand_id_number = random.randint(100000000, 999999999)

        # randomly pick one of the top-100 highest-valued soccer players as of now.
        # Used power law equation to prioritize higher valued players in the list
        # TODO: make a function out of power law equation in order to cache it and avoid creating it for every single instance.
        c_manual = 2.5  # Controls early steepness
        p_manual = 1.2  # Controls flattening
        n = 100  # list size
        rand_favorite_player = random.choices(
            fetch_top_100_players(verbose=False),
            k=1,
            weights=[
                1 / ((i + c_manual) ** p_manual) for i in range(n)
            ],
        )[0]["player_name"]

        rand_favorite_sport = random.choice(cls.sport_choices)[0]

        person = cls(
            name=fake_name,
            description=fake_description,
            has_kids=rand_has_kids,
            is_married=rand_is_married,
            dob=fake_dob,
            id_number=rand_id_number,
            favorite_player=rand_favorite_player,
            favorite_sport=rand_favorite_sport,
        )

        return person

    def __str__(self):
        return f"{self.name} ID:{self.id_number}"


"""
#### Faker Reference ####

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
