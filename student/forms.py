
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from student.models import CHOICES, StudentProfile
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

        )

    def clean_email(self):
        """
        ensure that email is always lower case.
        """
        return self.cleaned_data['email'].lower()


class UserContactFrom(forms.ModelForm):
    phone_no = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'input'}))

    class Meta:
        model = Typed
        fields = (
            'phone_no',
            'student_hall',
        )
    
    def clean_phone_no(self):
        phone_no = self.cleaned_data['phone_no']
        return phone_no

    def clean_user_group(self):
        user_group = self.cleaned_data['user_group']
        return user_group


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
class StudentProfileForm(forms.ModelForm):
    
    class Meta:
        model = StudentProfile
        fields = {
            'profile_image',
        }