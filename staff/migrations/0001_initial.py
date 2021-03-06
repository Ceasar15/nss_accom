# Generated by Django 3.2.4 on 2021-07-21 22:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='NewStudent',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('st_index_number', models.CharField(default='10203040', max_length=50)),
                ('gender', models.CharField(max_length=10)),
                ('room_number', models.CharField(max_length=10)),
                ('course', models.CharField(max_length=50)),
                ('level', models.CharField(max_length=50)),
                ('mobile_number', models.CharField(max_length=50)),
                ('images', models.ImageField(blank=True, upload_to='media/StudentImages/%Y/%m/%d/')),
                ('date_registered', models.DateTimeField(auto_now=True)),
                ('check_in', models.BooleanField(default=False)),
                ('hall', models.CharField(blank=True, default='No Hall', max_length=50, null=True)),
            ],
            options={
                'ordering': ['-date_registered'],
            },
        ),
        migrations.CreateModel(
            name='NewVisitor',
            fields=[
                ('vistor_id', models.AutoField(primary_key=True, serialize=False)),
                ('visiting_status', models.CharField(max_length=100)),
                ('visitor_index', models.CharField(blank=True, max_length=20, null=True)),
                ('visitor_fullName', models.CharField(max_length=150)),
                ('visiting_room', models.CharField(max_length=20)),
                ('room_member_getting_visited', models.CharField(max_length=150)),
                ('visiting_mobile_number', models.CharField(max_length=30)),
                ('visiting_date_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('visitor_in_out', models.CharField(default='in', max_length=10)),
                ('departed_at', models.DateTimeField(default=None, null=True)),
                ('hall', models.CharField(blank=True, default='No Hall', max_length=100, null=True)),
            ],
            options={
                'ordering': ['-visiting_date_time'],
            },
        ),
        migrations.CreateModel(
            name='UpdateVisitor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visitor_update', models.CharField(max_length=20)),
                ('visitor_one', models.OneToOneField(blank=True, default=2, null=True, on_delete=django.db.models.deletion.CASCADE, to='staff.newvisitor')),
            ],
        ),
        migrations.CreateModel(
            name='PostAnnouncement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_submitted', models.TimeField(auto_created=True, default=django.utils.timezone.now)),
                ('date_submitted', models.DateField(auto_created=True, default=django.utils.timezone.now)),
                ('announcement_title', models.CharField(max_length=100)),
                ('announcement_body', models.TextField()),
                ('annou_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date_submitted'],
            },
        ),
    ]
