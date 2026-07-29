from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.validators import validate_iranian_cellphone_number
from django.core.validators import RegexValidator


class UserType(models.IntegerChoices):
    customer = 1 , _("customer")
    admin = 2 , _("admin")
    superuser = 3 , _("superuser")



class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self,email,password,**extra_fields):
        """
        Creates and saves a User with the given email
        and password and extra data.
        """
        if not email:
            raise ValueError(_("the Email must be set"))
        user = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save()# using=self._db
        return user


    def create_superuser(self,email,password,**extra_fields):
        """
        Creates and saves a superuser with the given email
        and password and extra data.
        """
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_verified',True)
        extra_fields.setdefault('type',UserType.superuser.value)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password,**extra_fields)




class User(AbstractBaseUser,PermissionsMixin):
    """
    Custom User Model for our app
    """
    email = models.EmailField(_("email address"),unique=True)
    # is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    type = models.ImageField(choices=UserType.choices,default=UserType.customer.value)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    objects = UserManager()

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField('User',on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=12,validators=[validate_iranian_cellphone_number])

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)