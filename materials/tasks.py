from datetime import timezone, timedelta

from celery import shared_task
from django.contrib.auth import get_user_model

from materials.models import Course

@shared_task
def distribution(pk, user):
    if user.is_subscribe:
        instance = Course.objects.filter(pk=pk).first()

    if instance:
        update = False
        for upd in instance.course.all():
            if upd != instance.course.last_update():
                update = True

        if update == True:
            print('Один из ваших курсов обновлен')


User = get_user_model()


@shared_task
def block_inactive_users():
    # Определяем порог времени (30 дней назад)
    one_month_ago = timezone.now() - timedelta(days=30)

    inactive_users = User.objects.filter(
        is_active=True,
        is_staff=False,
        is_superuser=False,
        last_login__lt=one_month_ago
    )

    count = inactive_users.update(is_active=False)

    return f"Заблокировано пользователей: {count}"

