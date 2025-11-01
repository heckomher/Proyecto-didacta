from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('DOCENTE', 'Docente'),
        ('UTP', 'UTP'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='DOCENTE')

    def __str__(self):
        return f"{self.username} ({self.role})"

# Create your models here.
