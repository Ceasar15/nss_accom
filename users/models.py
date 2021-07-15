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


class UserType(models.Model):

	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='ut')
	user_type = models.CharField(max_length=8, choices=CHOICES, default='owner')
	# user_group = models.CharField(max_length=20, choices=CHOICES, default='student')


	class Meta:
		unique_together = ('user', 'user_type')


class ContactDetails(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	phone_no = models.IntegerField()


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()