from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.db import transaction


class StudentRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    user_type = forms.ChoiceField(choices=CHOICES, widget=forms.Select(attrs={'class':''}))
    
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2',
            'user_type',
        )
    
    @transaction.atomic                 
    def save(self):
        user = super().save(commit=False) 
        user.student = True            
        user.save()       
        
        return user