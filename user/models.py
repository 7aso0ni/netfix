from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.core.validators import MinLengthValidator, EmailValidator

from .managers import CustomerManager


# Create your models here.
class Customer(AbstractBaseUser):
    # the db fields
    username = models.CharField(
        max_length=30,
        validators=[MinLengthValidator(1, "Username can't be empty")],
        unique=True,
    )
    email = models.EmailField(
        max_length=255,
        validators=[EmailValidator("Invalid email address")],
        unique=True,
    )
    password = models.CharField(
        max_length=255, validators=[MinLengthValidator(1, "password can't be empty")]
    )
    date_of_birth = models.DateField()
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomerManager()

    #  default unique field that will be used to login will the email
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "password", "date_of_birth"]

    # clean will be called when full_clean is called it will not run automatically
    def clean(self):
        """provides validation to the data before storing in DB"""

        if self.date_of_birth == "" or None:
            raise ValidationError("date of birth can't be empty")

        # check if the given date is in the future
        if self.date_of_birth > timezone.now().date():
            raise ValidationError("Date of birth cannot be in the future")

        # this will check if the user is older than 18
        age = relativedelta(timezone.now().date(), self.date_of_birth).years
        if age < 18:
            raise ValidationError("User must be 18 years or older")

    def has_perm(self, perm: str, obj=None) -> bool:
        if self.is_superuser:
            return True

        if self.is_staff:
            if perm.startswith("user.delete_"):
                return False
            return True

        return False

    def has_module_perms(self, app_label):
        if self.is_superuser:
            return True

        if self.is_staff:
            allowed_apps: list[str] = ["user"]
            return app_label in allowed_apps

    # the object representation of the class instance
    def __str__(self):
        return self.username

    # @property
    # def is_staff(self) -> bool:
    #     "Is the user a member of staff?"
    #     # Simplest possible answer: All admins are staff
    #     return self._is_staff

    # @is_staff.setter
    # def is_staff(self, value):
    #     self._is_staff = value

    class Meta:
        # you can set the name of the database table instead of having django make the default value
        # you can also set whether to get data in an acending or a decending order
        # this will also provide the option give indexes and other DB objects.
        indexes = [
            models.Index(fields=["username"], name="username_idx"),
            models.Index(fields=["email"], name="email_idx"),
        ]
