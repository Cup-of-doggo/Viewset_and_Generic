from datetime import timezone, timedelta

from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def distribution(course_id, user_id):
    from materials.models import Course, Subscription
    from django.contrib.auth import get_user_model

    User = get_user_model()
    course = Course.objects.filter(pk=course_id).first()
    user = User.objects.filter(pk=user_id).first()

    if not course or not user:
        return

    # Проверяем подписку через модель Subscription
    subscription = Subscription.objects.filter(
        user=user, course=course, is_subscribe=True
    ).first()

    if subscription and subscription.is_subscribe:
        send_mail(
            subject=f"Обновление курса {course.course_name}",
            message=f"Курс {course.course_name} был обновлен. Проверьте новые материалы!",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )


@shared_task
def block_inactive_users():
    # Определяем порог времени (30 дней назад)
    one_month_ago = timezone.now() - timedelta(days=30)
    User = get_user_model()

    inactive_users = User.objects.filter(
        is_active=True, is_staff=False, is_superuser=False, last_login__lt=one_month_ago
    )

    count = inactive_users.update(is_active=False)

    return f"Заблокировано пользователей: {count}"
