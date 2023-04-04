import os

from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email
from django.db import models
from django.utils.translation import gettext_lazy as _
from versatileimagefield.fields import VersatileImageField
from versatileimagefield.placeholder import OnDiscPlaceholderImage


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        validate_email(email)
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    title = models.CharField(verbose_name=_("Title"), max_length=255, blank=True, null=True)
    company_name = models.CharField(verbose_name=_("Company Name"), max_length=255)
    phone = models.CharField(verbose_name=_("Phone Number"), max_length=30)
    description = RichTextUploadingField(verbose_name=_("Description"), null=True, blank=True)
    avatar = VersatileImageField(
        verbose_name=_("Avatar"),
        upload_to='user/avatars/',
        blank=True, null=True,
        placeholder_image=OnDiscPlaceholderImage(
            path=os.path.join(settings.BASE_DIR, "static", "placeholders", "no-image.png")
        )
    )
    childhood_photo = VersatileImageField(
        verbose_name=_("Childhood Photo"),
        upload_to='user/childhood_photos/',
        blank=True, null=True,
        placeholder_image=OnDiscPlaceholderImage(
            path=os.path.join(settings.BASE_DIR, "static", "placeholders", "no-image.png")
        )
    )
    updated = models.DateTimeField(
        verbose_name=_("Updated Date"),
        auto_now=True,
    )
    show_in_team_members = models.BooleanField(verbose_name=_("Show in Team Members"), default=False)
    order = models.IntegerField(default=0)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self) -> str:
        return f'{self.get_full_name()} [{self.email}]'
