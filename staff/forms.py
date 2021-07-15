from django import forms
from django.forms import fields
from .models import GENDER_PREF, LEVEL_CHOICES, VISITOR_STATUS, NewStudent, NewVisitor, PostAnnouncement, StudentImages


class PostAnnoumcementForm(forms.ModelForm):
    announcement_title = forms.CharField(max_length=100)
    announcement_body = forms.Textarea()
    # user_group  = forms.CharField(max_length=30, widget=forms.Select(choices= CHOICES))
    
    class Meta:
        model = PostAnnouncement
        # fields = '__all__'
        fields = (

            'announcement_title',
            'announcement_body',
        
        )
        exclude = (
            'date_submitted',
            'time_submitted',
        )

class StudentImagesForm(forms.ModelForm):
    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class':'file-input','multiple':True}), required=False)

    class Meta:
        model = StudentImages
        fields = ['images']