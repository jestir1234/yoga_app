from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.hashers import make_password
from .managers import CustomUserManager
import bcrypt

class User(AbstractBaseUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, error_messages={
                              'unique': 'This email address is already in use.'})
    password = models.CharField(max_length=128)
    USER_TYPE_CHOICES = [
        ('normal', 'Normal'),
        ('teacher', 'Teacher'),
    ]
    type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    studio_name = models.CharField(max_length=100, blank=True, null=True)
    studio_location = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def set_password(self, password):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.password = hashed_password.decode('utf-8')

    def save(self, *args, **kwargs):
        if not self.id:
            self.set_password(self.password)
        super().save(*args, **kwargs)
