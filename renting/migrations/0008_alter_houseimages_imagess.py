# Generated by Django 3.2.4 on 2021-07-27 18:24

from django.db import migrations, models
import renting.models


class Migration(migrations.Migration):

    dependencies = [
        ('renting', '0007_newrentalhouse_date_registered'),
    ]

    operations = [
        migrations.AlterField(
            model_name='houseimages',
            name='imagess',
            field=models.ImageField(blank=True, upload_to=renting.models.house_images),
        ),
    ]
