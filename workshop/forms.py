from django import forms
from .models import Workshop


class WorkshopForm(forms.ModelForm):
    class Meta:
        model = Workshop
        fields = ['title', 'date', 'price',
                  'description', 'location', 'photo', 'payment_link']

    def clean_photo(self):
        photo = self.cleaned_data.get('photo', False)
        if photo:
            # Check the file type
            if not photo.content_type or not photo.content_type.startswith('image'):
                raise forms.ValidationError('File type is not image')
            # Check the file size
            if photo.size > 10 * 1024 * 1024:
                raise forms.ValidationError('File size exceeds limit')
            return photo
        else:
            raise forms.ValidationError('Could not read the uploaded file')

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
