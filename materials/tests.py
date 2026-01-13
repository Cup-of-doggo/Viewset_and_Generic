from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from materials.models import Course, Lesson, Subscription
from django.urls import reverse
from unittest.mock import patch
from django.test import TestCase
from materials.tasks import distribution
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):

        self.user = get_user_model().objects.create(email="test@test.ru")
        self.user.set_password('password')
        self.user.save()
        self.course = Course.objects.create(course_name="test_course", owner=self.user)
        self.lesson = Lesson.objects.create(lesson_name='first_test_name',owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_create_lesson(self):
        data = {'lesson_name': 'test_name',
            'link':'https://www.youtube.com/',}
        response = self.client.post(reverse('materials:lesson_create'), data=data)
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            response.data['lesson_name'],
            'test_name'
        )

    def test_update_lesson(self):
        data = {'lesson_name': 'new_test_name',
                'link':'https://www.youtube.com/'}
        url = reverse('materials:lesson_update', args=[self.lesson.pk])
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['lesson_name'], 'new_test_name')

    def test_list_lesson(self):
        url = reverse('materials:lesson_list')
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.data['results'][0]['lesson_name'],
            self.lesson.lesson_name
        )

    def test_retrieve_lesson(self):
        url = reverse('materials:lesson_get', args=[self.lesson.pk])
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.data['lesson_name'],
            'first_test_name'
        )

    def test_destroy_lesson(self):
        url = reverse('materials:lesson_delete', args=[self.lesson.pk])
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        self.assertFalse(Lesson.objects.filter(pk=self.lesson.pk).exists())

    def test_unauthorized_user(self):
        self.client.force_authenticate(user=None)
        url = reverse('materials:lesson_list')
        response = self.client.get(url)
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED
        )

class IsOwnerOrStaffTestCase(APITestCase):
    def setUp(self):
        self.owner = User.objects.create(email='owner@test.com', password='password')
        self.other_user = User.objects.create(email='other@test.com', password='password')

        self.lesson = Lesson.objects.create(
            lesson_name='Owner Lesson',
            owner=self.owner
        )

    def test_update_with_user_without_access(self):
        self.client.force_authenticate(user=self.other_user)
        url = reverse('materials:lesson_update', args=[self.lesson.pk])
        data = {'lesson_name': 'New Name'}
        response = self.client.patch(url, data=data)
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )


class DistributionTaskTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(email='student@example.com')
        self.course = Course.objects.create(course_name="test_course")

    @patch('materials.tasks.send_mail')
    def test_distribution_send_email_success(self, mock_send_mail):

        Subscription.objects.create(user=self.user, course=self.course, is_subscribe=True)
        distribution(self.course.pk, self.user.pk)
        self.assertTrue(mock_send_mail.called)
        args, kwargs = mock_send_mail.call_args
        self.assertIn(f'Обновление курса {self.course.course_name}', kwargs['subject'])
        self.assertEqual(kwargs['recipient_list'], [self.user.email])

    @patch('materials.tasks.send_mail')
    def test_distribution_no_subscription(self, mock_send_mail):

        distribution(self.course.pk, self.user.pk)
        mock_send_mail.assert_not_called()
