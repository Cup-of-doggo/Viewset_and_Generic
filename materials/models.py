from django.db import models


class Lesson(models.Model):
    lesson_name = models.CharField(max_length=255, verbose_name="Название урока", null=True)
    lesson_description = models.TextField(verbose_name="Описание урока", blank=True, null=True)
    lesson_image = models.ImageField(upload_to="картинки/", verbose_name="Превью урока", null=True, blank=True)
    link = models.URLField(max_length=500, verbose_name="Ссылка на видео", blank=True)

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.lesson_name, self.lesson_description



class Course(models.Model):
    course_name = models.CharField(max_length=255, verbose_name="Название курса")
    course_image = models.ImageField(upload_to="картинки/", verbose_name="Превью курса", null=True, blank=True)
    course_description = models.TextField(verbose_name="Описание курса", blank=True, null=True)
    lesson_in_course = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name="Уроки курса", null=True)

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.course_name



