from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.db import transaction
from student.models import CHOICES

class StudentRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_no = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'input'}))
    user_group  = forms.CharField(max_length=30, widget=forms.Select(choices= CHOICES))
    
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
            'user_group',
        )
    
    @transaction.atomic                 
    def save(self):
        user = super().save(commit=False) 
        user.student = True            
        user.save()       
        
        return user

class EditProfileForm(UserChangeForm):
    phone_no = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'input'}))

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            'phone_no',
        ]
