# Generated by Django 3.2.4 on 2021-08-15 17:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_profile_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='nrh',
        ),
    ]
