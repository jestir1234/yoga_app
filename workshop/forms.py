from django import forms
from .models import Workshop, User
from PIL import Image
from django.core.exceptions import ValidationError

class WorkshopForm(forms.ModelForm):
    class Meta:
        model = Workshop
        fields = ['title', 'date', 'price',
                  'description', 'location', 'photo', 'payment_link']

    def clean_photo(self):
        photo = self.cleaned_data.get('photo', False)
        def clean_photo(self):
            if photo:
                try:
                    image = Image.open(photo)
                    image.verify()
                except Exception as e:
                    raise ValidationError("Please upload a valid image.")

                if not photo.content_type.startswith('image'):
                    raise ValidationError("Please upload a valid image.")
            return photo

    def save(self, commit=True):
        workshop = super().save(commit=False)
        if self.cleaned_data.get('photo'):
            photo_path = 'workshop_photos/{}'.format(
                self.cleaned_data['photo'].name)
            workshop.photo = photo_path
            with open(photo_path, 'wb') as f:
                f.write(self.cleaned_data['photo'].read())
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
