# Generated by Django 3.2.4 on 2021-07-20 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0003_newstudent_hall'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newstudent',
            name='hall',
            field=models.CharField(blank=True, default='No Hall', max_length=50, null=True),
        ),
    ]