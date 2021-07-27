# Generated by Django 3.2.4 on 2021-07-23 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('renting', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='househas',
            name='region',
            field=models.CharField(choices=[('Greater Accra Region', 'Greater Accra Region'), ('Ashanti Region', 'Ashanti Region'), ('Western North Region', 'Western North Region'), ('Western Region', 'Western Region'), ('Volta Region', 'Volta Region'), ('Eastern Region', 'Eastern Region'), ('Upper East Region', 'Upper East Region'), ('North East Region', 'North East Region'), ('Ahafo Region', 'Ahafo Region'), ('Bono Region', 'Bono Region'), ('Savannah Region', 'Savannah Region'), ('Bono East Region', 'Bono East Region'), ('Oti Region', 'Oti Region'), ('Northern Region', 'Northern Region'), ('Upper West Region', 'Upper West Region'), ('Central Region', 'Central Region')], default='Greater Accra Region', max_length=100),
        ),
    ]