# from model_practice.models.mp_02_relationships_n_inheritance_practice import (
#     Amp,
#     AmpOwner,
#     House,
#     Per,
#     PerAddr,
# )
from django.db import connection
import json
import inspect
from datetime import date, timedelta
import random

# from model_practice.models.mp_03_making_queries import (
#     Author,
#     Blog,
#     Entry,
# )


def blog_data_loader(filename=None):
    """
    helper function to load instance data
    particularly useful for shell use
    """

    # Read the JSON file
    if filename is None:
        filename = "model_practice/json/blog_instance_data.json"
    with open(filename, "r") as file:
        blogs_data = json.load(file)

    # Create Blog instances
    for blog_data in blogs_data:
        blog = Blog(
            **blog_data
        )  # Unpack the dictionary into the model fields
        blog.save()  # Save the instance to the database

    print("Blogs have been created successfully!")


def author_data_loader(filename=None):
    """
    helper function to load instance data
    particularly useful for shell use
    """

    # Read the JSON file
    if filename is None:
        filename = "model_practice/json/author_instance_data.json"
    with open(filename, "r") as file:
        authors_data = json.load(file)

    # Create Author instances
    for author_data in authors_data:
        author = Author(
            **author_data
        )  # Unpack the dictionary into the model fields
        author.save()  # Save the instance to the database

    print("Authors have been created successfully!")


def entry_data_loader(filename=None):
    """
    helper function to load instance data
    particularly useful for shell use
    """

    # Read the JSON file
    if filename is None:
        filename = "model_practice/json/entry_instance_data.json"
    with open(filename, "r") as file:
        entries_data = json.load(file)

    entries = []
    # Create Entry instances
    for entry_data in entries_data:
        entry = Entry(
            **entry_data
        )  # Unpack the dictionary into the model fields
        entries.append(entry)

    # Define your desired date range
    start_date = date(2020, 1, 1)
    end_date = date(2025, 12, 31)

    # Get all blogs and authors (converted to lists for efficiency)
    blogs = list(Blog.objects.all())
    authors = list(Author.objects.all())

    # First loop: assign pub_date and a random blog, then save each Entry
    for entry in entries:
        entry.pub_date = _random_date(start_date, end_date)
        entry.blog = random.choice(blogs)
        entry.save()

    # Second loop: for each Entry, add a random number of authors (without duplicates)
    all_entries = Entry.objects.all()
    for entry in all_entries:
        # Choose a random number between 1 and the total number of authors
        if authors:
            num_authors = random.randint(1, len(authors))
            # random.sample returns a list of unique authors
            selected_authors = random.sample(authors, num_authors)
            for author in selected_authors:
                entry.authors.add(author)
        # (Many-to-many changes are applied immediately; an extra save() is not required)
    print("Entries have been created successfully!")


def mass_loader():
    """
    utility function to load up all functions in current module
    and return all entries created but not saved
    """

    # fn_list = list(globals().values())

    # # remove mass_loader from fn_list to avoid infinite loop
    # fn_list.remove(globals()["mass_loader"])
    # # remove mass_deleter as it it does not make sense here
    # fn_list.remove(globals()["mass_deleter"])
    # # remove entry_data_loader to manually invoke later and pick
    # # the Entry list as a return value since we did not save them
    # # to the database
    # fn_list.remove(globals()["entry_data_loader"])
    # # remove reseting of the table indices
    # fn_list.remove(globals()["_reset_sqlite_sequences"])
    # # remove _random_date
    # fn_list.remove(globals()["_random_date"])

    # for fn in fn_list:
    #     if inspect.isfunction(fn):
    #         fn()
    # globals()["entry_data_loader"]()
    blog_data_loader()
    author_data_loader()
    entry_data_loader()


def django_doc_loader():
    beatles = Blog.objects.create(name="Beatles Blog")
    pop = Blog.objects.create(name="Pop Music Blog")
    Entry.objects.create(
        blog=beatles,
        headline="New Lennon Biography",
        pub_date=date(2008, 6, 1),
    )
    Entry.objects.create(
        blog=beatles,
        headline="New Lennon Biography in Paperback",
        pub_date=date(2009, 6, 1),
    )
    Entry.objects.create(
        blog=pop,
        headline="Best Albums of 2008",
        pub_date=date(2008, 12, 15),
    )
    Entry.objects.create(
        blog=pop,
        headline="Lennon Would Have Loved Hip Hop",
        pub_date=date(2020, 4, 1),
    )
    Author.objects.create(name="Alex", email="letsiki@gmail.com")
    Author.objects.create(name="John", email="john@msn.com")


def mass_deleter():
    Author.objects.all().delete()
    Entry.objects.all().delete()
    Blog.objects.all().delete()
    # Amp.objects.all().delete()
    # AmpOwner.objects.all().delete()
    # House.objects.all().delete()
    # Per.objects.all().delete()
    # PerAddr.objects.all().delete()
    # Person.objects.all().delete()
    _reset_sqlite_sequences()


def _reset_sqlite_sequences():
    with connection.cursor() as cursor:
        # Use Django's introspection to get all table names
        tables = connection.introspection.table_names()

        # Loop through each table and reset the sequence if its name
        # starts with 'model_practice_'
        for table in tables:
            if table.startswith("model_practice_"):
                cursor.execute(
                    f"UPDATE sqlite_sequence SET seq = 0 WHERE name = '{table}';"
                )


def reset_sqlite_sequences(*, tablename: str, app_name):
    if not tablename:
        raise ValueError("Invalid table name")
    with connection.cursor() as cursor:
        # Use Django's introspection to get all table names
        tables = connection.introspection.table_names()

        if (table := app_name + "_" + tablename) in tables:
            cursor.execute(
                f"UPDATE sqlite_sequence SET seq = 0 WHERE name = '{table}';"
            )
            print(f"successfully reset {table} table to index 0")
        else:
            print(f"table {table} not found")


def _random_date(start, end):
    delta = end - start
    random_days = random.randint(0, delta.days)
    return start + timedelta(days=random_days)
