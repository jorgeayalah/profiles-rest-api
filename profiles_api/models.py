from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin #this one gives us permission to modify the default djando user model
from django.contrib.auth.models import BaseUserManager


class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""
    def create_user(self, email, name, password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError('Users must have an email address')
        #Standarize second half of email to nonsensitive
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password) #this encryptes the password via AbstractBaseUser function (Django)
        user.save(using=self._db)   #standard procedure to store in Django

        return user
    
    def create_superuser(self, email, name, password):
        """Create and ssvae a new superuser with given details"""
        user = self.create_user(email, name, password)

        user.is_superuser = True    #even tho this is not initially defined in the class, PermissionMixion allows it
        user.is_staff = True
        user.save(using=self._db)

        return user



class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)   #to access special functions

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def getFullName(self):
        """Retrieve full name of user"""
        return self.name
    
    def getShortName(self):
        """Retrieve short name of user"""
        return self.name #momentarily
    
    def __str__(self):  #this function is recommended to receive a meaninful output when converting the model
        """Return string representation of our user"""
        return self.email

