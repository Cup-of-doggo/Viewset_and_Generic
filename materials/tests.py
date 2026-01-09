from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from materials.models import Course

class LessonTestCase(APITestCase):

    def setUp(self):

        self.user = get_user_model().objects.create(email="test@test.ru")
        self.user.set_password('password')
        self.user.save()
        self.course = Course.objects.create(course_name="test_course", owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_create_lesson(self):
        data = {
            'lesson_name':'test_name',
            'lesson_description':'test_text',
            'lesson_image':'test_image',
            'link':'youtube.com',
            'course':self.course.id
        }

        response = self.client.post('/lesson/create/', data=data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
