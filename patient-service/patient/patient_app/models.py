from django.db import models
from django.contrib.auth.hashers import make_password

class Patient(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=128)  # Store hashed password

    def save(self, *args, **kwargs):
        if self.pk is None:  # Only hash the password when creating a new patient
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
