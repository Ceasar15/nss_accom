from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
import django_filters


GENDER_PREF = (
    ('M','MALE'),
    ('F','FEMALE'),
    ('O','OTHERS')
)

LEVEL_CHOICES = (
    ('M','MALE'),
    ('F','FEMALE'),
    ('O','OTHERS')
)

VISITOR_STATUS = (
    ('STUDENT','STUDENT'),
    ('NON-STUDENT','NON-STUDENT'),
    ('O','OTHERS')
)

class NewStudent(models.Model):
    index_number = models.CharField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10, choices=GENDER_PREF)
    room_number = models.CharField(max_length=10)
    course = models.CharField(max_length=50)
    level = models.CharField(max_length=50, choices=LEVEL_CHOICES)
    mobile_number = models.CharField(max_length=50)
    date_added_registered = models.DateTimeField()
    check_in = models.BooleanField()


class StudentImages(models.Model):
    images = models.ImageField(upload_to='media/StudentImages/%Y/%m/%d/', blank=True)
    new_student= models.ForeignKey(NewStudent, on_delete=models.CASCADE)


class PostAnnouncement(models.Model):
    announcement_id = models.AutoField()
    announcement_title = models.CharField(max_length=100)
    announcement_body = models.TextField()
    date_submitted = models.DateField()
    time_submitted = models.TimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class NewVisitor(models.Model):
    vistor_id = models.AutoField(primary_key=True)
    visiting_status = models.CharField(max_length=100, choices=VISITOR_STATUS)
    visitor_fullName = models.CharField(max_length=150)
    visiting_room = models.CharField(max_length=20)
    room_member_getting_visited = models.CharField(max_length=150)
    visiting_mobile_number = models.CharField(max_length=30)
    visiting_date_time = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
