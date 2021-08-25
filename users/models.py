from cloudinary.models import CloudinaryField
from django.db import models
from django.contrib.auth.models import User
from users.managers import UT
from django.dispatch import receiver
from django.db.models.signals import post_save

CHOICES = (
    ('student','student'),
    ('staff','staff'),
    ('landlord', 'landlord'),
)


class Typed(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    user_group = models.CharField(max_length=20, choices=CHOICES)
    phone_no = models.IntegerField(null=True)
    student_hall = models.CharField(max_length=100, default='No Hall', blank=True, null=True)

    class Meta:
        unique_together = ('user_id', 'user_group')

class ContactDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_no = models.IntegerField()
        

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=30, null=True, blank=True)
    occupation = models.CharField(max_length=190, null=True, blank=True)
    profile_image = CloudinaryField('image',  default='default.jpeg', blank=True, null=True)

class Contact(models.Model):
    fullname = models.CharField(max_length=190)
    phone = models.CharField(max_length=90)
    email = models.EmailField(max_length=190)
    message = models.TextField()
