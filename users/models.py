from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    avatar = models.ImageField(
        upload_to="users/", verbose_name="Аватар", null=True, blank=True
    )
    phone = models.CharField(
        max_length=20, verbose_name="Телефон", null=True, blank=True
    )
    city = models.CharField(max_length=100, verbose_name="Город", null=True, blank=True)
    last_login = models.DateTimeField(
        "дата последнего входа", auto_now=False, null=True, blank=True
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email, self.avatar


class Payments(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, verbose_name="Пользователь"
    )
    payment_date = models.DateField(verbose_name="Дата оплаты")
    paid_course = models.ForeignKey(
        Course, on_delete=models.PROTECT, verbose_name="Оплаченный курс"
    )
    payment_summ = models.IntegerField(verbose_name="Сумма оплаты")
    session_id = models.AutoField(primary_key=True)
    link = models.URLField(
        max_length=50, verbose_name="Ссылка на оплату", blank=True, null=True
    )

    CASH = "cash"
    CARD = "card"

    payment_choice = [
        (CASH, "Наличными"),
        (CARD, "По карте"),
    ]

    payment_method = models.CharField(
        max_length=20, verbose_name="Способ оплаты", choices=payment_choice
    )

    class Meta:
        verbose_name = "Оплата"
        verbose_name_plural = "Оплаты"

    def __str__(self):
        return (
            f"Пользователь: {self.user}, дата оплаты: {self.payment_date}, "
            f"сумма оплаты: {self.payment_summ}, оплаченный курс: {self.paid_course}, оплата {self.payment_method}"
        )
