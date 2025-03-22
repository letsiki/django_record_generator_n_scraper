from django.db import models

from app_one.models import Person

# TODO: Practice O2O and Abstract Class Inheritance
# - [X] O2O with and without parent_link (Place-Restaurant, Passport-Person)
# - [X] Test null=True with both
# - [X] Test table behavior with both
# - [X] Import a model from another app
# - [X] Override `save` method, verify `bulk_create`
# - [X] Meta is inherited by default, to extend we must do so explicitly. Test
# - [X] In case of multiple inheritance only the first Meta is inherited unless specified explicitly. Use pass if not extension is needed. Test
# - [X] An abstract class with a FK or M2M relationship would make reverse lookups ambiguous, practice with '%(app_label)s' and '%(class)s'


class Passport(models.Model):
    number = models.IntegerField()
    passenger = models.OneToOneField(
        "Passenger", on_delete=models.CASCADE
    )


class Passenger(models.Model):
    name = models.CharField(max_length=30)


class Place(models.Model):
    address = models.CharField(max_length=100)


class Restaurant(models.Model):
    cuisine_choices = {
        "chinese": "Chinese",
        "italian": "Italian",
        "greek": "Greek",
    }
    cuisine = models.CharField(max_length=15, choices=cuisine_choices)
    place = models.OneToOneField(
        Place, parent_link=True, on_delete=models.CASCADE
    )

    def save(self, **kwargs):
        if self.cuisine == "greek":
            print("greek restaurants are not accepted here")
            return
        else:
            super().save(**kwargs)


class Dog(models.Model):
    text = models.CharField(max_length=30)


class A(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        abstract = True
        verbose_name_plural = "plural"


class B(models.Model):
    name2 = models.CharField(max_length=30)
    relationship = models.ForeignKey(
        Dog, on_delete=models.CASCADE, related_name="%(class)sB"
    )
    # if no related name and query name are specified it will work fine as the child class name will be use to construct the reverse name and query name. If it is though we need to make it dynamic otherwise it will be common among children this is blocked by migration if missed.

    class Meta:
        abstract = True
        verbose_name = "singular"
        ordering = ["name2"]


class C(A, B):
    age = models.IntegerField()

    class Meta(A.Meta, B.Meta):
        ordering = (B.Meta.ordering + ["age"])[::-1]


class D(A, B):
    age2 = models.IntegerField()

    class Meta(A.Meta, B.Meta):
        ordering = (B.Meta.ordering + ["age2"])[::-1]
