# Generated by Django 3.2.4 on 2021-07-19 16:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0003_updatevisitor'),
    ]

    operations = [
        migrations.RenameField(
            model_name='updatevisitor',
            old_name='visitor',
            new_name='visitor_one',
        ),
    ]
