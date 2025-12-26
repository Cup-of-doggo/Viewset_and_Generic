from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Email")
    avatar = models.ImageField(upload_to="users/", verbose_name="Аватар", null=True, blank=True)
    phone = models.CharField(max_length=20, verbose_name="Телефон", null=True, blank=True)
    city = models.CharField(max_length=100, verbose_name="Город", null=True, blank=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email, self.avatar

