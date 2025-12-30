from django.urls import path
from rest_framework.routers import DefaultRouter
from users.views import PaymentsListApiView

router = DefaultRouter()

urlpatterns = [
    path('payments/', PaymentsListApiView.as_view(), name='payments_list'),
] + router.urls