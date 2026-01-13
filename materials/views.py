from rest_framework import viewsets, generics
from materials.models import Course, Lesson
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
            course=updated_course,
            is_subscribe=True
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
                course=course,
                is_subscribe=True
            )
            for subscription in subscriptions:
                distribution.delay(course.pk, subscription.user.pk)

class LessonDestroyApiView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsOwnerOrStaff]


