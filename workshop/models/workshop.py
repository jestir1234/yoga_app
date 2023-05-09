from django.db import models
from django.utils import timezone
from .users import User


class Workshop(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField(default=timezone.now)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    location = models.CharField(max_length=255)
    payment_link = models.URLField(blank=True, null=True)
    photo = models.ImageField(
        upload_to='workshop_photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
