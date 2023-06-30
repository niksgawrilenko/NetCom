from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class Package(models.Model):
    name = models.CharField(max_length=255)
    speed = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Channel(models.Model):
    icon = models.ImageField(upload_to='channel_icons')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class TVPackage(models.Model):
    name = models.CharField(max_length=255)
    channels = models.ManyToManyField(Channel)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_channel_count(self):
        return self.channels.count()

class Additional(models.Model):
    icon = models.ImageField(upload_to='additional_icons/')
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Equipment(models.Model):
    icon = models.ImageField(upload_to='equipment_icons/')
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name




class Subscriber(AbstractUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    balance = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    password = models.CharField(max_length=100)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    tv_package = models.ForeignKey(TVPackage, on_delete=models.CASCADE)
    additional = models.ManyToManyField(Additional, blank=True)
    equipment = models.ManyToManyField(Equipment, blank=True)

    REQUIRED_FIELDS = ['name', 'phone', 'address', 'balance', 'password', 'package', 'tv_package']
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='user_subscriber_set',
        related_query_name='user_subscriber'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='user_subscriber_set',
        related_query_name='user_subscriber'
    )
    def __str__(self):
        return self.name