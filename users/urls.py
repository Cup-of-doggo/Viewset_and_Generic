from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from users.views import PaymentsListApiView, UserCreateApiView
from .apps import UsersConfig
from .views import MyTokenObtainPairView

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r'Payments', PaymentsListApiView, basename='payments_list')


urlpatterns = [
    path('users/', UserCreateApiView.as_view(), name='user_create'),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + router.urls
