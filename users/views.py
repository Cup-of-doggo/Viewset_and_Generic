from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from users.models import Payments
from users.serializers import PaymentsSerializer, MyTokenObtainPairSerializer, UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class PaymentsListApiView(generics.ListAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'payment_method')
    ordering_fields = ('payment_date')
    permission_classes = [IsAuthenticated]

class UserCreateApiView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer