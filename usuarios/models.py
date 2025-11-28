#from django.db import models

# Create your models here.
# usuarios/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    activation_token = models.CharField(max_length=64, blank=True, null=True)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username" 
    REQUIRED_FIELDS = ["email"] 

    def __str__(self):
        return self.username