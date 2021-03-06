from cloudinary.models import CloudinaryField
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

COMPLAINT_STATUS = (
    ('PENDING','PENDING'),
    ('APPROVED','APPROVED'),
    ('DECLINED','DECLINED')
)


CHOICES = (
	('student','Student'),
	('staff','Staff'),
	('landlord', 'Landlord'),
)



class NewComplaint(models.Model):
    complaint_id = models.AutoField(primary_key=True)
    student_index_number = models.CharField(max_length=20)
    student_full_name = models.CharField(max_length=150)
    student_room_number = models.CharField(max_length=10)
    complaint_type = models.CharField(max_length=50)
    complaint_description = models.TextField()
    mobile_number = models.CharField(max_length=11)
    date_submitted = models.DateTimeField(default=timezone.now)
    complaint_status = models.CharField(max_length=20, choices=COMPLAINT_STATUS, default='PENDING')
    student_hall = models.CharField(max_length=50, default='No_Hall', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)


    class Meta:
        ordering = ['-date_submitted']

    def __str__(self):
        return self.student_index_number
        

class StudentProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_image = CloudinaryField('image', default='default.jpeg')
    