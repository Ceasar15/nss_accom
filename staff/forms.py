from django import forms
from django.forms import fields
from .models import GENDER_PREF, LEVEL_CHOICES, NewStudent, NewVisitor, PostAnnouncement, UpdateVisitor


class PostAnnoumcementForm(forms.ModelForm):
    announcement_title = forms.CharField(max_length=100)
    announcement_body = forms.Textarea()
    
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



class NewStudentForm(forms.ModelForm):
    st_index_number = forms.CharField(max_length=15)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    gender = forms.ChoiceField(choices=GENDER_PREF)
    room_number = forms.CharField(max_length=10)
    course = forms.CharField(max_length=50)
    level = forms.ChoiceField(choices=LEVEL_CHOICES)
    mobile_number = forms.CharField(max_length=50)

    class Meta:
        model = NewStudent
        fields = (

        'first_name',
        'last_name',
        'st_index_number',
        'room_number',
        'gender',
        'level',
        'course',
        'mobile_number',
        'images',
        'hall',
        )
    
        exclude = (
            'date_registered',
            'check_in',
        )



class NewVisitorForm(forms.ModelForm):

    class Meta:
        model = NewVisitor
        fields = (
            'visiting_status',
            'visitor_fullName',
            'visiting_room',
            'room_member_getting_visited',
            'visiting_mobile_number',
            'hall',
        )
        exclude = (
            'visiting_date_time',
            'visitor_in_out',
        )

    def visiting_status(self):
        visiting_status = self.cleaned_data['visiting_status']
        return visiting_status



class UpdateVisitorForm(forms.ModelForm):

    class Meta():
        model = UpdateVisitor
        fields = (
            'visitor_update',
        )
    
