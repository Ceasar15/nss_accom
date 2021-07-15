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
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='ut')
    # user_type = models.CharField(max_length=8, choices=CHOICES, default='owner')
    user_group = models.CharField(max_length=20, choices=CHOICES, default='student')
    phone_no = models.IntegerField(default='0000000000')


    def __str__(self):
        return self.phone_no

    # class Meta:
    #     unique_together = ('user', 'user_group')


class ContactDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_no = models.IntegerField()
            

@receiver(post_save, sender=User)
def create_user_type(sender, instance, created, **kwargs):
    if created:
        Typed.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_type(sender, instance, **kwargs):
    instance.typed.save()
