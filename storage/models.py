from django.contrib.auth.models import User
from django.db import models

user1 = User.objects.get(username='paluch@wp.pl')


class Person(models.Model):
    first_name = models.CharField(max_length=64, verbose_name='')
    last_name = models.CharField(max_length=64, verbose_name='')
    description = models.TextField(max_length=200, null=True, verbose_name='', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Address(models.Model):
    city = models.CharField(max_length=64, verbose_name='')
    street = models.CharField(max_length=64, verbose_name='')
    house_number = models.SmallIntegerField(verbose_name='')
    flat_number = models.SmallIntegerField(null=True, verbose_name='')
    person_address = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='addresses')


TYPE = ((1, 'Home'), (2, 'Business'), (3, 'Mobile'), (4, 'Other'))


class Phone(models.Model):
    number = models.BigIntegerField(verbose_name='', blank=True)
    number_type = models.SmallIntegerField(choices=TYPE, verbose_name='', blank=True)
    person_number = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='numbers')


EMAIL_TYPE = ((1, 'Personal'), (2, 'Business'), (3, 'Other'))


class Email(models.Model):
    address = models.EmailField(max_length=64, verbose_name='', blank=True)
    email_type = models.SmallIntegerField(choices=EMAIL_TYPE, verbose_name='', blank=True)
    person_email = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='emails')


class Group(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True)
    members = models.ManyToManyField(Person)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
