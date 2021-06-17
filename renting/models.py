from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.

STATE_CHOICES = [

	('Greater Accra Region','Greater Accra Region'),
('Ashanti Region','Ashanti Region'),
('Western North Region','Western North Region'),
('Western Region','Western Region'),
('Volta Region','Volta Region'),
('Eastern Region','Eastern Region'),
('Upper East Region','Upper East Region'),
('North East Region','North East Region'),
('Ahafo Region','Ahafo Region'),
('Bono Region','Bono Region'),
('Savannah Region','Savannah Region'),
('Bono East Region','Bono East Region'),
('Oti Region','Oti Region'),
('Northern Region','Northern Region'),
('Upper West Region','Upper West Region'),
('Central Region','Central Region'),
]

HH_FIELD_CHOICES = (
		('Pr','Private'),
		('Sh','Shared'),
		('No','Not Available'),
	)

FIELD_CHOICES =(
		('Y','Yes'),
		('N','No')
)

GENDER_PREF = (
	('M','MALE'),
	('F','FEMALE'),
	('O','OTHERS')
)

ROOMS = (
	('zero',0),
	('one',1),
	('two',2),
	('three',3),
	('three_plus',4)

)


def house_images(instance, filename):
	return f'user_{instance.nrh.user.username}/{filename}'


class NewRentalHouse(models.Model):
    house_no = models.CharField(max_length=100)
    region = models.CharField(max_length=100, choices=STATE_CHOICES)
    street_address = models.TextField()
    city = models.CharField(max_length=150)
    area = models.CharField(max_length=150)
    # zipcode = models.CharField(max_length=12)
    country = models.CharField(max_length=100, default='Ghana')
    #longitude = models.DecimalField(max_digits=4, decimal_places=2)
    #latitude = models.DecimalField(max_digits=4, decimal_places=2)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    in_date = models.DateField()
    out_date = models.DateField()
    
    rent = models.PositiveIntegerField(default=100)

class HouseImages(models.Model):
	images = models.ImageField(upload_to=house_images, blank=True)
	nrh = models.ForeignKey(NewRentalHouse, on_delete=models.CASCADE)



class HouseHas(models.Model):

	bedroom = models.CharField(max_length=11, choices=ROOMS)
	kitchen = models.CharField(max_length=2, choices=HH_FIELD_CHOICES)
	bathroom = models.CharField(max_length=2, choices=HH_FIELD_CHOICES)
	living_room = models.CharField(max_length=2, choices=HH_FIELD_CHOICES)
	toilet = models.CharField(max_length=2, choices=HH_FIELD_CHOICES)
	balcony = models.CharField(max_length=2, choices=HH_FIELD_CHOICES)
	parking = models.CharField(max_length=2, choices=FIELD_CHOICES)
	nrh = models.OneToOneField(NewRentalHouse, on_delete=models.CASCADE) 

region = models.CharField(max_length=100, choices=STATE_CHOICES)

class Amenities(models.Model):

	bed = models.CharField(max_length=1, choices=FIELD_CHOICES)
	furnished = models.CharField(max_length=1, choices=FIELD_CHOICES)

	nrh = models.OneToOneField(NewRentalHouse, on_delete=models.CASCADE)


class PreferredTenant(models.Model):
	gender = models.CharField(max_length=1, choices=GENDER_PREF)
	nrh = models.OneToOneField(NewRentalHouse, on_delete=models.CASCADE)


class Rules(models.Model):
	smoking_allowed = models.CharField(max_length=1, choices=FIELD_CHOICES)
	musical_instrument = models.CharField(max_length=1, choices=FIELD_CHOICES)

	nrh = models.OneToOneField(NewRentalHouse, on_delete=models.CASCADE)

	# class Meta:
	# 	unique_together = ()




