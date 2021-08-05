from django import forms
from django.db.models import fields
from .models import (ContactLandlord, NewRentalHouse, HouseHas, 
    Amenities, Rules, PreferredTenant, STATE_CHOICES, HH_FIELD_CHOICES, 
    FIELD_CHOICES, GENDER_PREF, ROOMS, HouseImages, Rating, Payments)



class SearchForm(forms.Form):
    place = forms.CharField(widget=forms.TextInput(attrs={'class':'input' ,'placeholder':'Search place'}))


class RentalHouseForm(forms.ModelForm):

    house_no = forms.CharField(label='House No',widget=forms.TextInput(attrs={'class':'input', 'placeholder':'House No#'}))
    street_address = forms.CharField(label='Street Address',widget=forms.Textarea(attrs={'class':'input', 'placeholder':'Street Address'}))
    area = forms.CharField(widget=forms.TextInput(attrs={'class':'input', 'placeholder':'Area'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class':'input', 'placeholder':'City'}))
    region = forms.ChoiceField(label='REGION', choices=STATE_CHOICES, widget=forms.Select(attrs={'class':'multiple'}))
    country = forms.CharField(widget=forms.TextInput(attrs={'class':'input', 'placeholder':'Ghana'}), required=False)
    rent = forms.IntegerField(widget=forms.NumberInput())

    class Meta:
        model = NewRentalHouse
        fields = '__all__'
        exclude = ['user']


class HouseImagesForm(forms.ModelForm):
    images = forms.FileField(widget=forms.ClearableFileInput(attrs={'class':'file-input','multiple':True}), required=False)
    
    class Meta:
        model = HouseImages
        fields = ['images']

class HouseImagesEditForm(forms.ModelForm):
    imagess = forms.ImageField(widget=forms.FileInput(attrs={'class':'file-input','multiple':True}), required=False)

    class Meta:
        model = HouseImages
        fields = ['imagess']


# Defining all fields is hectic process

class HouseHasForm(forms.ModelForm):

    bedroom = forms.ChoiceField(label='Bedroom', choices=ROOMS)
    kitchen = forms.ChoiceField(choices=HH_FIELD_CHOICES, widget=forms.Select(attrs={'class':'multiple'}))
    bathroom = forms.ChoiceField(choices=HH_FIELD_CHOICES,widget=forms.Select(attrs={'class':'multiple'}))
    living_room = forms.ChoiceField(choices=HH_FIELD_CHOICES,widget=forms.Select(attrs={'class':'multiple'}))
    toilet = forms.ChoiceField(choices=HH_FIELD_CHOICES,widget=forms.Select(attrs={'class':'multiple'}))
    balcony = forms.ChoiceField(choices=HH_FIELD_CHOICES,widget=forms.Select(attrs={'class':'multiple'}))
    parking = forms.ChoiceField(choices=FIELD_CHOICES,widget=forms.Select(attrs={'class':'multiple'}))

    class Meta:
        model = HouseHas
        fields = '__all__'
        exclude = ['nrh']	

    def __init__(self, *args,**kwargs):
        super().__init__(*args,**kwargs)
        for visible in self.visible_fields():
            visible.field.label_classes=('field-label','is-small')


class AmenitiesForm(forms.ModelForm):

    #This method provides an easy way of definig the choices and widgets for the each field 
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'multiple'
            visible.field.choices = FIELD_CHOICES
            visible.field.label_classes = ('field-label','is-small',)

    class Meta:
        model = Amenities
        fields = '__all__'
        exclude = ['nrh']


class RulesForm(forms.ModelForm):

    class Meta:
        model = Rules
        fields = '__all__'
        exclude = ['nrh']

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        for visible in self.visible_fields():
            visible.field.choices = FIELD_CHOICES 


class PreferredTenantForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.choices = FIELD_CHOICES
        self.fields['gender'].choices = GENDER_PREF
    
    class Meta:
        model = PreferredTenant
        fields = '__all__'
        exclude = ['nrh']


class ContactLandlordForm(forms.ModelForm):

    class Meta:
        model = ContactLandlord
        fields = {
            'full_name',
            'email',
            'phone',
            'message',
        }

class RatingForm(forms.ModelForm):
    rating = forms.RadioSelect(attrs={'id': 'value'})
    class Meta:
        model = Rating
        fields = ('rating', 'comments')
            

class PaymentsForm(forms.ModelForm):
    class Meta:
        model = Payments
        fields = (
                'fullname',
                'email',
                'mobile_number',
                'types',
                'amount'
        )

    def clean_phone(self):
        fullname = self.cleaned_data['fullname']
        return fullname
    def clean_email(self):
        email = self.cleaned_data['email']
        return email
    def clean_mobile_number(self):
        mobile_number = self.cleaned_data['mobile_number']
        return mobile_number
    def clean_type(self):
        types = self.cleaned_data['types']
        return types
    def clean_amount(self):
        amount = self.cleaned_data['amount']
        return amount        
