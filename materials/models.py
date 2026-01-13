

from django.conf import settings
from django.db import models
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response


class Lesson(models.Model):
    lesson_name = models.CharField(max_length=255, verbose_name="Название урока", null=True)
    lesson_description = models.TextField(verbose_name="Описание урока", blank=True, null=True)
    lesson_image = models.ImageField(upload_to="картинки/", verbose_name="Превью урока", null=True, blank=True)
    link = models.URLField(max_length=500, verbose_name="Ссылка на видео", blank=True)
    course = models.ForeignKey("Course", on_delete=models.CASCADE, verbose_name="Курс", related_name="lessons", null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return f"{self.lesson_name}, {self.lesson_description}"

class Course(models.Model):
    course_name = models.CharField(max_length=255, verbose_name="Название курса")
    course_image = models.ImageField(upload_to="картинки/", verbose_name="Превью курса", null=True, blank=True)
    course_description = models.TextField(verbose_name="Описание курса", blank=True, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.course_name


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь", null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс", null=True)
    is_subscribe = models.BooleanField(verbose_name='Подписка',null=True, blank=True, default=False)

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f"{self.user}, {self.course}"

    def post(self, *args, **kwargs):

        user = self.requests
        course_id = self.requests.data
        course_item = get_object_or_404
        subs_item = user, course_id, course_item

        if subs_item.exists():
            message = 'подписка удалена'
        else:
            message = 'подписка добавлена'

        return Response({"message": message})