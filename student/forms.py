from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.db import transaction
from student.models import CHOICES

class StudentRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_no = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'input'}))
    
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2',
            'phone_no',
        )
    
    @transaction.atomic                 
    def save(self):
        user = super().save(commit=False) 
        user.student = True            
        user.save()       
        
        return user

class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password'
            'phone_no',
        ]
