from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

# Create your tests here.
from tasks.models import Task
from .models import TrainingSession


class TrainingFlowTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='secret123')
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        Task.objects.create(
            subject='math',
            topic='algebra',
            difficulty='easy',
            text='2+2=?',
            correct_answer='4',
        )
        Task.objects.create(
            subject='math',
            topic='algebra',
            difficulty='easy',
            text='3+3=?',
            correct_answer='6',
        )

    def test_training_start_submit_and_results(self):
        start_response = self.client.post(
            reverse('training-start'),
            {'subject': 'math', 'tasks_count': 2},
            format='json',
        )
        self.assertEqual(start_response.status_code, status.HTTP_201_CREATED)

        session_id = start_response.data['session_id']
        first_task = start_response.data['task']

        submit_first = self.client.post(
            reverse('training-submit'),
            {
                'session_id': session_id,
                'task_id': first_task['id'],
                'answer': Task.objects.get(id=first_task['id']).correct_answer,
            },
            format='json',
        )
        self.assertEqual(submit_first.status_code, status.HTTP_200_OK)
        self.assertFalse(submit_first.data['session_finished'])
        self.assertIn('next_task', submit_first.data)

        next_task = submit_first.data['next_task']
        submit_second = self.client.post(
            reverse('training-submit'),
            {
                'session_id': session_id,
                'task_id': next_task['id'],
                'answer': Task.objects.get(id=next_task['id']).correct_answer,
            },
            format='json',
        )

        self.assertEqual(submit_second.status_code, status.HTTP_200_OK)
        self.assertTrue(submit_second.data['session_finished'])
        self.assertIn('results', submit_second.data)

        results_response = self.client.get(reverse('training-results', kwargs={'session_id': session_id}))
        self.assertEqual(results_response.status_code, status.HTTP_200_OK)
        self.assertEqual(results_response.data['total_tasks'], 2)
        self.assertEqual(len(results_response.data['table']), 2)

        session = TrainingSession.objects.get(id=session_id)
        self.assertTrue(session.is_finished)