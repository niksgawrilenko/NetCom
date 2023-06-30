from django.contrib import admin
from django.contrib.auth.models import Group, Permission

# Register your models here.
from django.contrib import admin
from .models import Package, Subscriber, Additional, Channel, TVPackage, Equipment

admin.site.register(Package)
admin.site.register(Subscriber)
admin.site.register(Channel)
admin.site.register(TVPackage)
admin.site.register(Additional)
admin.site.register(Equipment)