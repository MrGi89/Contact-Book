from django.db import models


class Person(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    description = models.TextField(null=True)


class Address(models.Model):
    city = models.CharField(max_length=64)
    street = models.CharField(max_length=64)
    house_number = models.SmallIntegerField()
    flat_number = models.SmallIntegerField(null=True)
    person_address = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='addresses')


TYPE = ((1, 'Home phone'), (2, 'Business phone'), (3, 'Mobile phone'), (4, 'Other'))


class Phone(models.Model):
    number = models.BigIntegerField()
    number_type = models.SmallIntegerField(choices=TYPE)
    person_number = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='numbers')


EMAIL_TYPE = ((1, 'Home'), (2, 'Business'), (3, 'Other'))


class Email(models.Model):
    address = models.CharField(max_length=64)
    email_type = models.SmallIntegerField(choices=EMAIL_TYPE)
    person_email = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='emails')


class Group(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True)
    members = models.ManyToManyField(Person)
