from django.db import models
from django.contrib.auth.models import User
from users.managers import UT
from django.dispatch import receiver
from django.db.models.signals import post_save
from renting.models import NewRentalHouse

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

# @receiver(post_save, sender=User)
# def create_user_type(sender, instance, created, **kwargs):
#     if created:
#         Typed.objects.create(user_id=instance)

# @receiver(post_save, sender=User)
# def save_user_type(sender, instance, **kwargs):
#     instance.ut.save()



class ContactDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_no = models.IntegerField()
        

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=30)
    occupation = models.CharField(max_length=190)
    profile_image = models.ImageField(upload_to='landlord/profile_image/', blank=True)
    nrh = models.ForeignKey(NewRentalHouse, on_delete=models.CASCADE, null=True, blank=True) 