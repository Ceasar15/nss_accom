# Generated by Django 3.2.4 on 2021-07-15 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_typed_phone_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='typed',
            name='phone_no',
            field=models.IntegerField(default='00000', null=True),
        ),
    ]
