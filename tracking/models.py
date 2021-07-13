from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
import django_filters

from django.utils import timezone

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

COMPLAINT_STATUS = (
    ('PENDING','PENDING'),
    ('APPROVED','APPROVED'),
    ('DECLINED','DECLINED')
)

class NewStudent(models.Model):
    index_number = models.CharField(primary_key=True, max_length=11)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10, choices=GENDER_PREF)
    room_number = models.CharField(max_length=10)
    course = models.CharField(max_length=50)
    level = models.CharField(max_length=50, choices=LEVEL_CHOICES)
    mobile_number = models.CharField(max_length=50)
    date_registered = models.DateTimeField()
    check_in = models.BooleanField()

    class Meta:
        ordering = ['-date_registered']

    def __str__(self):
        return self.first_name
    

class StudentImages(models.Model):
    images = models.ImageField(upload_to='media/StudentImages/%Y/%m/%d/', blank=True)
    new_student= models.ForeignKey(NewStudent, on_delete=models.CASCADE)


class PostAnnouncement(models.Model):
#    announcement_id = models.AutoField()
    announcement_title = models.CharField(max_length=100)
    announcement_body = models.TextField()
    date_submitted = models.DateField(default=timezone.now)
    time_submitted = models.TimeField(default=timezone.now)
    annou_user = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        ordering = ['-date_submitted']

    def __str__(self):
        return self.announcement_title

class NewVisitor(models.Model):
    vistor_id = models.AutoField(primary_key=True)
    visiting_status = models.CharField(max_length=100, choices=VISITOR_STATUS)
    visitor_fullName = models.CharField(max_length=150)
    visiting_room = models.CharField(max_length=20)
    room_member_getting_visited = models.CharField(max_length=150)
    visiting_mobile_number = models.CharField(max_length=30)
    visiting_date_time = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-visiting_date_time']

    def __str__(self):
        return self.visitor_fullName

class NewComplaint(models.Model):
    complaint_id = models.AutoField(primary_key=True)
    student_index_number = models.CharField(max_length=20)
    student_full_name = models.CharField(max_length=150)
    student_room_number = models.CharField(max_length=10)
    complaint_type = models.CharField(max_length=50)
    complaint_description = models.TextField()
    mobile_number = models.CharField(max_length=11)
    date_submitted = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-date_submitted']

    def __str__(self):
        return self.student_index_number

class ComplaintStatus(models.Model):
    complaint_status_id = models.AutoField(primary_key=True)
    # who = models.OneToOneField(NewComplaint, on_delete=models.CASCADE)
    complaint_status = models.CharField(max_length=20, choices=COMPLAINT_STATUS, default='PENDING')
    submitted_by = models.OneToOneField(NewComplaint, on_delete=models.CASCADE)

    def __str__(self):
        return self.submitted_by