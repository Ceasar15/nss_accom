# Generated by Django 3.2.4 on 2021-07-29 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('renting', '0010_contactlandlord'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactlandlord',
            name='landlord_id',
            field=models.IntegerField(null=True),
        ),
    ]