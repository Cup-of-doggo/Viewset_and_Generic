from rest_framework import viewsets, generics
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import Course, Lesson, Subscription
from materials.paginators import LessonCoursePaginator
from materials.serializers import CourseSerializer, LessonSerializer
from rest_framework.permissions import IsAuthenticated

from materials.tasks import distribution
from users.permissions import IsOwnerOrStaff


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsOwnerOrStaff]
    pagination_class = LessonCoursePaginator

    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()

    def perform_update(self, serializer):
        updated_course = serializer.save()

        from materials.models import Subscription

        subscriptions = Subscription.objects.filter(
            course=updated_course, is_subscribe=True
        )
        for subscription in subscriptions:
            distribution.delay(updated_course.pk, subscription.user.pk)


class LessonCreateApiView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwnerOrStaff]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListApiView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = LessonCoursePaginator


class LessonRetrieveApiView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]


class LessonUpdateApiView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwnerOrStaff]

    def perform_update(self, serializer):
        lesson = serializer.save()
        if lesson.course:
            course = lesson.course
            course.save()

            from materials.models import Subscription

            subscriptions = Subscription.objects.filter(
                course=course, is_subscribe=True
            )
            for subscription in subscriptions:
                distribution.delay(course.pk, subscription.user.pk)


class LessonDestroyApiView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsOwnerOrStaff]


class SubscriptionAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course")
        course_item = get_object_or_404(Course, pk=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            message = "Подписка уже активирована"
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "Подписка добавлена"

        return Response({"message": message})
