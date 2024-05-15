from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


from .managers import CustomerManager
import datetime


# Create your models here.
class Customer(AbstractBaseUser):
    # the db fields
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomerManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "password", "date_of_birth"]

    # clean will be called when full_clean is called it will not run automatically
    def clean(self):
        # check if the given date is in the future
        if self.date_of_birth > timezone.now().date():
            raise ValidationError("Date of birth cannot be in the future")

        # this will check if the user is older than 18
        if timezone.now().date() - datetime.timedelta(18 * 365) < self.date_of_birth:
            raise ValidationError("User must be 18 years or older")

    # the object representation of the class instance
    def __str__(self):
        return self.username

    # @property
    # def is_staff(self):
    #     "Is the user a member of staff?"
    #     # Simplest possible answer: All admins are staff
    #     return self.is_staff

    class Meta:
        # you can set the name of the database table instead of having django make the default value
        # you can also set whether to get data in an acending or a decending order
        # this will also provide the option give indexes and other DB objects.
        models.indexes = [
            models.Index(fields=["username"], name="username_idx"),
            models.Index(fields=["email"], name="email_idx"),
        ]
