from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.db import transaction
from django.forms import fields
from student.models import CHOICES
from users.forms import Typed

class StudentRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2',
            # 'phone_no',
            # 'user_group',
        )
    
    # @transaction.atomic                 
    # def save(self):
    #     user = super().save(commit=False) 
    #     user.student = True            
    #     user.save()       
        
    #     return user

class UserContactFrom(forms.ModelForm):
    phone_no = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'input'}))
    user_group  = forms.CharField(max_length=30, widget=forms.Select(choices= CHOICES))

    class Meta:
        model = Typed
        fields = (
            'phone_no',
            'user_group'
        ) 


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
