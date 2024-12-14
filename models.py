from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager

class User(AbstractUser):
    
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True, null=False, default='anonymous')


    # 'email' heya el primary field mta3 authentication
    USERNAME_FIELD = 'email'

    # for creating a superuser; 'email' should be the only required field 
    REQUIRED_FIELDS = ['username'] 
    objects = UserManager()
    class Meta:
        db_table = 'security_app_user'