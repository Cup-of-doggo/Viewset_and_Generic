from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from users.models import Payments, User
from users.serializers import PaymentsSerializer, MyTokenObtainPairSerializer, UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from users.services import create_stripe_product, create_stripe_price, create_stripe_session



class PaymentsListApiView(viewsets.ModelViewSet):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["course", "lesson", "payment_method"]
    search_fields = ["user__email", "course__name"]
    ordering_fields = ["payment_date"]
    permission_classes = [IsAuthenticated]


    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        if payment.course is None and payment.lesson is None:
            raise ValidationError("Нужно выбрать курс или урок")
        elif payment.course and payment.lesson:
            raise ValidationError("Нужно выбрать либо курс, либо урок")
        else:
            if payment.course:
                product = create_stripe_product(payment.course)
            else:
                product = create_stripe_product(payment.lesson)
        price = create_stripe_price(stripe_product=product, amount=payment.amount)
        session_id, session_url = create_stripe_session(price)
        payment.session_id = session_id
        payment.link = session_url
        payment.save()

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserCreateApiView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]


class UserListApiView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        active_users = serializer.save(user=self.request.user)
        active_users.block_inactive_users()
        active_users.save()

class UserRetrieveApiView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

class UserUpdateApiView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

class UserDestroyApiView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

