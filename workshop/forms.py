from django import forms
from .models import Workshop, User
from PIL import Image
from django.core.exceptions import ValidationError


class WorkshopForm(forms.ModelForm):
    class Meta:
        model = Workshop
        fields = ['title', 'date', 'price', 'time',
                  'description', 'location', 'photo', 'payment_link']

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if not date:
            raise forms.ValidationError("Please enter a valid date.")
        return date

    def clean_time(self):
        time = self.cleaned_data.get('time')
        if not time:
            raise forms.ValidationError("Please enter a valid time.")
        return time


    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo:
            try:
                image = Image.open(photo.file)
                image.verify()
            except Exception as e:
                raise forms.ValidationError("Please upload a valid image.")

            if not photo.content_type.startswith('image'):
                raise forms.ValidationError("Please upload a valid image.")
        return photo


    def save(self, commit=True):
        workshop = super().save(commit=False)
        if self.cleaned_data.get('photo'):
            photo = self.cleaned_data['photo']
            workshop.photo.save(photo.name, photo)
        if commit:
            workshop.save()
            self.save_m2m()
        return workshop


class PersonalInfoForm(forms.ModelForm):
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    email = forms.EmailField(label='Email')
    studio_name = forms.CharField(label='Studio Name')
    studio_location = forms.CharField(label='Studio Location')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email',
                  'studio_name', 'studio_location']
