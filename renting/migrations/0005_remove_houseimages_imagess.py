# Generated by Django 3.2.4 on 2021-07-27 12:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('renting', '0004_houseimages_imagess'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='houseimages',
            name='imagess',
        ),
    ]