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


TYPE = ((1, 'home phone'), (2, 'business phone'), (3, 'mobile phone'), (4, 'other'))


class Phone(models.Model):
    number = models.SmallIntegerField()
    number_type = models.SmallIntegerField(choices=TYPE)
    person_number = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='numbers')


EMAIL_TYPE = ((1, 'home'), (2, 'business'), (3, 'other'))


class Email(models.Model):
    address = models.CharField(max_length=64)
    email_type = models.SmallIntegerField(choices=TYPE)
    person_email = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='emails')
