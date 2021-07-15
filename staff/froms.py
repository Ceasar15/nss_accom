from django import forms
from .models import GENDER_PREF, LEVEL_CHOICES, VISITOR_STATUS, NewStudent, NewVisitor, PostAnnouncement, StudentImages



class StudentImagesForm(forms.ModelForm):
	images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class':'file-input','multiple':True}), required=False)

	class Meta:
		model = StudentImages
		fields = ['images']