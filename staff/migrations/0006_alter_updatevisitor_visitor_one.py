# Generated by Django 3.2.4 on 2021-07-19 16:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0005_alter_updatevisitor_visitor_one'),
    ]

    operations = [
        migrations.AlterField(
            model_name='updatevisitor',
            name='visitor_one',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='staff.newvisitor'),
        ),
    ]
