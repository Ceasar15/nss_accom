
from django.db import models
from django.contrib.auth.models import User
from users.managers import UT


CHOICES = (
	('student','Student'),
	('staff','Staff'),
	('landlord', 'Landlord'),
)


class UserType(models.Model):

	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='ut')
	user_type = models.CharField(max_length=8, choices=CHOICES, default='owner')


	class Meta:
		unique_together = ('user', 'user_type')


class ContactDetails(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	phone_no = models.IntegerField()
