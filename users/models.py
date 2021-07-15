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
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True, blank=True, related_name='ut')
    user_group = models.CharField(max_length=20, choices=CHOICES, null=True, default='student')
    phone_no = models.IntegerField(max_length=50 ,default='9000000008', null=True)


    def __str__(self):
        return self.phone_no

    # class Meta:
    #     unique_together = ('user', 'user_group')

@receiver(post_save, sender=User)
def create_user_type(sender, instance, created, **kwargs):
    if created:
        Typed.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_type(sender, instance, **kwargs):
    instance.ut.save()



class ContactDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_no = models.IntegerField()
            