from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Q
import django_filters

from django.utils import timezone

GENDER_PREF = (
    ('M','MALE'),
    ('F','FEMALE'),
)

LEVEL_CHOICES = (
    ('100','100'),
    ('200','200'),
    ('300','300'),
    ('400', '400'),
    ('Graduate', 'Graduate')
)

VISITOR_STATUS = (
    ('STUDENT','STUDENT'),
    ('NON-STUDENT','NON-STUDENT'),
    ('O','OTHERS')
)



class NewStudent(models.Model):
    index_number = models.CharField(primary_key=True, max_length=11)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    st_index_number = models.CharField(max_length=50, default='10203040')
    gender = models.CharField(max_length=10)
    room_number = models.CharField(max_length=10)
    course = models.CharField(max_length=50)
    level = models.CharField(max_length=50)
    mobile_number = models.CharField(max_length=50)
    images = models.ImageField(upload_to='media/StudentImages/%Y/%m/%d/', blank=True)
    date_registered = models.DateTimeField(auto_now=True)
    check_in = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_registered']

    def __str__(self):
        return self.first_name
    

# class StudentImages(models.Model):
#     new_student= models.ForeignKey(NewStudent, on_delete=models.CASCADE)


class PostAnnouncement(models.Model):
    announcement_title = models.CharField(max_length=100)
    announcement_body = models.TextField()
    date_submitted = models.DateField(auto_created=True, default=timezone.now)
    time_submitted = models.TimeField(auto_created=True, default=timezone.now)
    annou_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    class Meta:
        ordering = ['-date_submitted']

    def __str__(self):
        return self.announcement_title

class NewVisitor(models.Model):
    vistor_id = models.AutoField(primary_key=True)
    visiting_status = models.CharField(max_length=100)
    visitor_index = models.CharField(max_length=20, blank=True, null=True)
    visitor_fullName = models.CharField(max_length=150)
    visiting_room = models.CharField(max_length=20)
    room_member_getting_visited = models.CharField(max_length=150)
    visiting_mobile_number = models.CharField(max_length=30)
    visiting_date_time = models.DateTimeField(default=timezone.now)
    visitor_in_out = models.CharField(max_length=10, default='in')
    


    class Meta:
        ordering = ['-visiting_date_time']

    def __str__(self):
        return self.visitor_fullName


class UpdateVisitor(models.Model):
    visitor_one = models.OneToOneField(NewVisitor, on_delete=models.CASCADE, default=2, null=True, blank=True)
    visitor_update = models.CharField(max_length=20)

    def __str__(self):
        return self.visitor


# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         NewVisitor.objects.create(user=instance)
    
# @receiver(post_save, sender=User)
# def save_profile(sender, instance, **kwargs):
#     instance.staff_newvisitor.save()

