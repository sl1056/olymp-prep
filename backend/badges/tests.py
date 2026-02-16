from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from analytics.models import TaskAttempt
from pvp.models import Match
from tasks.models import Task

from .models import Badge, UserBadge


class BadgesApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='u1', password='pass123')
        self.opponent = User.objects.create_user(username='u2', password='pass123')
        self.client.force_authenticate(user=self.user)

        self.math_task = Task.objects.create(
            subject='math',
            topic='algebra',
            difficulty='easy',
            text='2+2?',
            correct_answer='4',
        )

        self.subject_badge = Badge.objects.create(
            title='Математик',
            description='Решить 2 задачи по математике с точностью 50%',
            type='subject',
            condition_subject='math',
            condition_min_solved=2,
            condition_min_correct_ratio=0.5,
            icon='🧮',
        )
        self.total_badge = Badge.objects.create(
            title='Активный',
            description='Решить 3 задачи',
            type='total',
            condition_total_solved=3,
            icon='⭐',
        )
        self.pvp_badge = Badge.objects.create(
            title='Победитель PvP',
            description='Выиграть 1 матч',
            type='pvp',
            condition_min_solved=1,
            icon='⚔️',
        )

    def test_badges_endpoint_returns_progress_shape_for_frontend(self):
        response = self.client.get(reverse('user-badges'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

        item = response.data[0]
        self.assertIn('progress', item)
        self.assertIn('completed', item)
        self.assertIn('bgColor', item)
        self.assertIn('difficultyLevel', item)

    def test_task_attempt_earns_subject_badge_via_signal(self):
        TaskAttempt.objects.create(user=self.user, task=self.math_task, is_correct=True, subject='math', difficulty='easy')
        TaskAttempt.objects.create(user=self.user, task=self.math_task, is_correct=False, subject='math', difficulty='easy')

        user_badge = UserBadge.objects.get(user=self.user, badge=self.subject_badge)
        self.assertEqual(user_badge.status, 'earned')

    def test_total_badge_progress_and_status(self):
        for _ in range(3):
            TaskAttempt.objects.create(
                user=self.user,
                task=self.math_task,
                is_correct=True,
                subject='math',
                difficulty='easy',
            )

        response = self.client.get(reverse('user-badges'))
        total = next(item for item in response.data if item['id'] == self.total_badge.id)
        self.assertEqual(total['status'], 'earned')
        self.assertEqual(total['progress']['solved'], 3)
        self.assertEqual(total['progress']['needed'], 3)

    def test_pvp_badge_earned_on_real_win(self):
        Match.objects.create(
            player1=self.user,
            player2=self.opponent,
            status='finished',
            task=self.math_task,
            player1_correct=True,
            player2_correct=False,
        )

        user_badge = UserBadge.objects.get(user=self.user, badge=self.pvp_badge)
        self.assertEqual(user_badge.status, 'earned')

        response = self.client.get(reverse('user-badges'))
        pvp = next(item for item in response.data if item['id'] == self.pvp_badge.id)
        self.assertEqual(pvp['status'], 'earned')
        self.assertEqual(pvp['progress']['solved'], 1)
