from users.models import Profile
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
import django_filters
from cloudinary.models import CloudinaryField
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
    country = models.CharField(max_length=100, default='Ghana')
    date_registered = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    landlord_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    rent = models.PositiveIntegerField(default=100)

image_dafault = 'img/default.jpg'

class HouseImages(models.Model):
    imagess = CloudinaryField('image', blank=True, default=image_dafault)
    nrh = models.ForeignKey(NewRentalHouse, on_delete=models.CASCADE)

    def images(self):
        if self.imagess and hasattr(self.imagess, 'url'):
            return self.imagess.url

class HouseHas(models.Model):

    bedroom = models.CharField(max_length=11, choices=ROOMS)
    kitchen = models.CharField(max_length=2, choices=HH_FIELD_CHOICES)
    bathroom = models.CharField(max_length=2, choices=HH_FIELD_CHOICES)
    living_room = models.CharField(max_length=2, choices=HH_FIELD_CHOICES)
    toilet = models.CharField(max_length=2, choices=HH_FIELD_CHOICES)
    balcony = models.CharField(max_length=2, choices=HH_FIELD_CHOICES)
    parking = models.CharField(max_length=2, choices=FIELD_CHOICES)
    nrh = models.OneToOneField(NewRentalHouse, on_delete=models.CASCADE) 

    region = models.CharField(max_length=100, choices=STATE_CHOICES, default="Greater Accra Region")

class Amenities(models.Model):

    bed = models.CharField(max_length=1, choices=FIELD_CHOICES)
    furnished = models.CharField(max_length=1, choices=FIELD_CHOICES)

    nrh = models.OneToOneField(NewRentalHouse, on_delete=models.CASCADE)


class PreferredTenant(models.Model):
    gender = models.CharField(max_length=1, choices=GENDER_PREF)
    nrh = models.OneToOneField(NewRentalHouse, on_delete=models.CASCADE)
    description = models.TextField(default='Massa tempor nec feugiat nisl pretium. Egestas fringilla phasellus faucibus scelerisque eleifend donec Porta nibh venenatis cras sed felis eget velit aliquet. Neque volutpat ac tincidunt vitae semper quis lectus. Turpis in eu mi bibendum neque egestas congue quisque. Sed elementum tempus egestas sed sed risus pretium quam. Dignissim sodales ut eu sem. Nibh mauris cursus mattis molesteeiaculis at erat pellentesque. Id interdum velit laoreet id donec', null=True, blank=True)


class Rules(models.Model):
    smoking_allowed = models.CharField(max_length=1, choices=FIELD_CHOICES)
    musical_instrument = models.CharField(max_length=1, choices=FIELD_CHOICES)

    nrh = models.OneToOneField(NewRentalHouse, on_delete=models.CASCADE)


class SearchFilter(django_filters.FilterSet):
    city = django_filters.CharFilter(method='custom_filter')
    class Meta:
        model = NewRentalHouse
        fields = {
            'rent': ['gt', 'lt']
        }
    
    def custom_filter(self, queryset, name, value):
        return NewRentalHouse.objects.filter(
            Q(city__icontains=value) | Q(area__icontains=value) | Q(region__icontains=value) 
        )

class ContactLandlord(models.Model):
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    landlord_id = models.IntegerField(null=True, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    

class Rating(models.Model):
    landlord = models.ForeignKey(NewRentalHouse, default=None, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.CharField(max_length=50)
    comments = models.CharField(max_length=100)
    date = models.DateTimeField(auto_created=True, auto_now=True)


class Payments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)    
    fullname= models.CharField(max_length=100, null=True)
    email= models.EmailField(max_length=110, null=True)
    mobile_number= models.CharField(null=True, max_length=15)
    amount= models.IntegerField(null=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(self.fullname)
    
    class Meta:
        ordering = ["-created_on"]
