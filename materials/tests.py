from rest_framework import status
from rest_framework.test import APITestCase


class LessonTestCase(APITestCase):

    def setUp(self) -> None:
        pass

    def test_create_lesson(self):
        data = {
            'lesson_name':'test_name',
            'lesson_description':'test_text',
            'lesson_image':'test_image',
            'link':'test_link',
            'course':'test_course'
        }

        response = self.client.post('/lesson/create/', data=data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
