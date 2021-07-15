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
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True, related_name='ut')
    user_group = models.CharField(max_length=20, choices=CHOICES)
    phone_no = models.IntegerField(null=True)




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
            