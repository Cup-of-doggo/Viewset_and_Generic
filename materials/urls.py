from django.urls import path

from materials.apps import MaterialsConfig
from rest_framework.routers import DefaultRouter

from materials.views import CourseViewSet, LessonCreateApiView, LessonListApiView, LessonRetrieveApiView, \
    LessonUpdateApiView, LessonDestroyApiView

app_name = MaterialsConfig.name


router = DefaultRouter
router.register(r'Course', CourseViewSet, basename='course')




urlpatterns = [
    path('lesson/create/', LessonCreateApiView, name='lesson_create'),
    path('lesson/', LessonListApiView.as_view(), name='lesson_list'),
    path('lesson/<int:pk>/', LessonRetrieveApiView.as_view(), name='lesson_get'),
    path('lesson/update/<int:pk>/', LessonUpdateApiView.as_view(), name='lesson_update'),
    path('lesson/delete/<int:pk>/', LessonDestroyApiView.as_view(), name='lesson_delete'),
] + router.urls

