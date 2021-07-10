from django import forms
from django.contrib.auth.models import User
from users.models import UserType, CHOICES, ContactDetails
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.db import transaction

class UserTypeForm(forms.ModelForm):
	user_type = forms.ChoiceField(choices=CHOICES, widget=forms.Select(attrs={'class':''}))
	class Meta:
		model = UserType
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
        )
    
    @transaction.atomic                 
    def save(self):
        user = super().save(commit=False) 
        user.is_client = True            
        user.is_admin = False
        user.save()       
        
        return user
    
class StaffRegisterForm(UserCreationForm):
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
        )

    @transaction.atomic  
    def save(self):
        user = super().save(commit=False)
        user.is_admin = True 
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