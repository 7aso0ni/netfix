from django.contrib.auth.models import BaseUserManager


class CustomerManager(BaseUserManager):
    def create_user(self, email: str, password: str, **extra_fields: dict):
        if not email:
            raise ValueError("User must have an email address")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

    # This method allows Django to fetch the user instance using the email field
    def get_by_natural_key(self, email: str | None) -> str:
        """
        This method allows Django to fetch a Customer object using the email field as the "natural key".
        It takes an email address as input and returns the corresponding Customer object. This method is used internally by Django for certain operations,
        such as handling user authentication.
        """
        return self.get(email=email)
