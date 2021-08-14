from django import forms
from django.contrib.auth.models import User
from django.db.models import fields
from numpy import mod
from users.models import Contact, Typed, CHOICES, ContactDetails, Profile
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.db import transaction




class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = {
            'location',
            'occupation',
            'profile_image',
        }

class UserTypeForm(forms.ModelForm):
    user_type = forms.ChoiceField(choices=CHOICES, widget=forms.Select(attrs={'class':''}))
    class Meta:
        model = Typed
        fields = ['user_type']


class UserForm(forms.ModelForm):

    username = forms.CharField(widget=forms.TextInput(attrs={'class':'input'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'input'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'input'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'input'}))

    class Meta:
        model = User
        exclude = ['password', 'last_login','is_superuser','is_staff','user_permissions','groups','date_joined', 'is_active']



class UpdatePhoneNo(forms.ModelForm):
    phone_no = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'input'}))

    class Meta:
        model = ContactDetails
        fields = ['phone_no']

CHOICES = (
	('Student','Student'),
	('Staff','Staff'),
	('Landlord', 'Landlord'),
)
    
class StaffRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
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
            'user_group',
        )

    def clean_email(self):
        """
        ensure that email is always lower case.
        """
        return self.cleaned_data['email'].lower()


    @transaction.atomic  
    def save(self):
        user = super().save(commit=False)
        user.staff = True 
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
        ]

class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = {
            'fullname',
            'phone',
            'email',
            'message',
        }