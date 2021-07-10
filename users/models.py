
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import related
from users.managers import UT


class UserType(AbstractUser):
    is_student = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)


CHOICES = (
	('owner','Owner'),
	('tenant','Student')
)


class UserType(models.Model):

	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='ut')
	user_tye = models.CharField(max_length=6, choices=CHOICES, default='owner')


	class Meta:
		unique_together = ('user', 'user_tye')


class ContactDetails(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	phone_no = models.IntegerField()
