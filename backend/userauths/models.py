from typing import Iterable
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save

from shortuuid.django_fields import ShortUUIDField

class User(AbstractUser):
    """
    Custom user model that extends AbstractUser.
    
    Attributes:
        username (str): The username of the user.
        email (str): The email address of the user.
        full_name (str): The full name of the user.
        phone (str): The phone number of the user.
    """
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        """
        Returns the string representation of the user, which is the email address.
        """
        return self.email
    
    def save(self, *args, **kwargs):
        """
        Overrides the save method to set default values for full_name and username
        based on the email address if they are not provided.
        """
        email_username, mobile = self.email.split('@')
        if self.full_name == "" or self.full_name is None:
            self.full_name = email_username
        if self.username == "" or self.username is None:
            self.username = email_username

        super(User, self).save(*args, **kwargs)


class Profile(models.Model):
    """
    Profile model that extends the user model with additional attributes.
    
    Attributes:
        user (User): The user associated with the profile.
        image (FileField): The profile image of the user.
        full_name (str): The full name of the user.
        about (str): A brief description about the user.
        gender (str): The gender of the user.
        country (str): The country of the user.
        state (str): The state of the user.
        city (str): The city of the user.
        address (str): The address of the user.
        date (date): The date the profile was created.
        pid (ShortUUIDField): A unique identifier for the profile.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(upload_to="image", default="default/default-user.jpg", blank=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    about = models.TextField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(max_length=100, blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    pid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefghijklmnopqrstuvwxyz")

    def __str__(self):
        """
        Returns the string representation of the profile, which is the full name
        if available, otherwise the user's full name.
        """
        if self.full_name:
            return str(self.full_name)
        else:
            return str(self.user.full_name)
        
    def save(self, *args, **kwargs):
        """
        Overrides the save method to set the default value for full_name
        based on the user's full name if it is not provided.
        """
        if self.full_name == "" or self.full_name is None:
            self.full_name = self.user.full_name

        super(Profile, self).save(*args, **kwargs)

def create_user_profile(sender, instance, created, **kwargs):
    """
    A signal that creates a profile for a user when a user is created.
    """
    if created:
        print(f"Creating profile for user: {instance.email}")
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    """
    A signal that saves the profile when the user is saved.
    """
    print(f"Saving profile for user: {instance.email}")
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)