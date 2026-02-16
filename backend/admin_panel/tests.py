from io import BytesIO
from unittest.mock import patch

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from pvp.models import Match
from tasks.models import Task


class AdminPanelApiTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username='admin', password='pass123', is_staff=True)
        self.user = User.objects.create_user(username='student', password='pass123')
        self.client.force_authenticate(user=self.admin)

        self.task = Task.objects.create(
            subject='math',
            topic='algebra',
            difficulty='easy',
            text='2+2?',
            correct_answer='4',
            hints=['Сложи два и два'],
        )

    def test_admin_can_list_and_update_users(self):
        users_url = reverse('admin-users-list')
        response = self.client.get(users_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)

        detail_url = reverse('admin-users-detail', kwargs={'pk': self.user.id})
        update_response = self.client.patch(
            detail_url,
            {'is_active': False, 'role': 'admin'},
            format='json',
        )
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)
        self.assertTrue(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_non_admin_cannot_access_admin_endpoints(self):
        self.client.force_authenticate(user=self.user)
        users_url = reverse('admin-users-list')

        response = self.client.get(users_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_create_update_and_delete_task(self):
        tasks_url = reverse('admin-tasks-list')

        create_response = self.client.post(
            tasks_url,
            {
                'subject': 'phys',
                'topic': 'mechanics',
                'difficulty': 'medium',
                'text': 'Что такое сила?',
                'correct_answer': 'ma',
                'hints': ['Второй закон Ньютона'],
            },
            format='json',
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        created_id = create_response.data['id']

        detail_url = reverse('admin-tasks-detail', kwargs={'pk': created_id})
        patch_response = self.client.patch(detail_url, {'topic': 'dynamics'}, format='json')
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_response.data['topic'], 'dynamics')

        delete_response = self.client.delete(detail_url)
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

    def test_admin_can_get_match_results_and_external_api_status(self):
        Match.objects.create(
            player1=self.admin,
            player2=self.user,
            task=self.task,
            status='finished',
            player1_correct=True,
            player2_correct=False,
        )

        matches_url = reverse('admin-matches-results')
        matches_response = self.client.get(matches_url)
        self.assertEqual(matches_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(matches_response.data), 1)
        self.assertEqual(matches_response.data[0]['winner'], self.admin.username)

        check_url = reverse('admin-external-api-check')

        class MockResponse(BytesIO):
            status = 200

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc_val, exc_tb):
                self.close()

        with patch('admin_panel.views.urlopen', return_value=MockResponse(b'')):
            check_response = self.client.post(
                check_url,
                {'url': 'https://example.com/health'},
                format='json',
            )

        self.assertEqual(check_response.status_code, status.HTTP_200_OK)
        self.assertTrue(check_response.data['reachable'])
        self.assertEqual(check_response.data['status_code'], 200)
