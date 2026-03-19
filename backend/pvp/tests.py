from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase

<<<<<<< Updated upstream
# Create your tests here.
=======
from tasks.models import Task
from .consumers import MatchConsumer
from .models import Match


class PvpConsumerLogicTests(TestCase):
    def setUp(self):
        self.player1 = User.objects.create_user(username='p1', password='123')
        self.player2 = User.objects.create_user(username='p2', password='123')
        self.task = Task.objects.create(
            subject='math',
            topic='algebra',
            difficulty='easy',
            text='2+2?',
            correct_answer='4',
        )
        self.second_task = Task.objects.create(
            subject='math',
            topic='algebra',
            difficulty='easy',
            text='3+3?',
            correct_answer='6',
        )
        self.match = Match.objects.create(
            player1=self.player1,
            player2=self.player2,
            status='active',
            task=self.task,
        )

    def _make_consumer(self, user):
        consumer = MatchConsumer()
        consumer.user = user
        consumer.match_id = self.match.id
        return consumer

    def test_duplicate_submission_is_ignored(self):
        consumer = self._make_consumer(self.player1)

        first_submit = consumer._save_answer_to_db('4')
        second_submit = consumer._save_answer_to_db('5')

        self.match.refresh_from_db()

        self.assertTrue(first_submit['accepted'])
        self.assertFalse(first_submit['both_submitted'])
        self.assertFalse(second_submit['accepted'])
        self.assertEqual(second_submit['reason'], 'Ответ уже отправлен')
        self.assertEqual(self.match.player1_answer, '4')
        self.assertTrue(self.match.player1_correct)

    def test_finalize_match_is_idempotent(self):
        consumer_p1 = self._make_consumer(self.player1)
        consumer_p2 = self._make_consumer(self.player2)

        consumer_p1._save_answer_to_db('4')
        self.assertTrue(consumer_p2._save_answer_to_db('4')['both_submitted'])

        first = consumer_p1._finalize_match_logic(self.match.id)
        p1_rating_after_first = self.player1.profile.rating
        p2_rating_after_first = self.player2.profile.rating

        second = consumer_p1._finalize_match_logic(self.match.id)

        self.player1.profile.refresh_from_db()
        self.player2.profile.refresh_from_db()

        self.assertEqual(first['match_id'], second['match_id'])
        self.assertEqual(first['winner'], second['winner'])
        self.assertEqual(self.player1.profile.rating, p1_rating_after_first)
        self.assertEqual(self.player2.profile.rating, p2_rating_after_first)

    def test_match_moves_to_next_question_before_finish(self):
        self.match.questions_count = 2
        self.match.question_task_ids = [self.task.id, self.second_task.id]
        self.match.save(update_fields=['questions_count', 'question_task_ids'])

        consumer_p1 = self._make_consumer(self.player1)
        consumer_p2 = self._make_consumer(self.player2)

        consumer_p1._save_answer_to_db('4')
        self.assertTrue(consumer_p2._save_answer_to_db('5')['both_submitted'])

        after_first_round = consumer_p1._finalize_match_logic(self.match.id)
        self.match.refresh_from_db()

        self.assertEqual(after_first_round['event'], 'next_question')
        self.assertEqual(self.match.status, 'active')
        self.assertEqual(self.match.current_question_index, 2)
        self.assertEqual(self.match.task_id, self.second_task.id)
        self.assertEqual(self.match.player1_score, 1)
        self.assertEqual(self.match.player2_score, 0)
        self.assertIsNone(self.match.player1_submitted_at)
        self.assertIsNone(self.match.player2_submitted_at)

        consumer_p1._save_answer_to_db('6')
        self.assertTrue(consumer_p2._save_answer_to_db('6')['both_submitted'])

        finished = consumer_p1._finalize_match_logic(self.match.id)
        self.match.refresh_from_db()

        self.assertEqual(finished['event'], 'finished')
        self.assertEqual(self.match.status, 'finished')
        self.assertEqual(finished['winner'], 'player1')
        self.assertEqual(finished['total_questions'], 2)
        self.assertEqual(finished['player1_score'], 2)
        self.assertEqual(finished['player2_score'], 1)


class PvpApiTests(APITestCase):
    def setUp(self):
        self.player1 = User.objects.create_user(username='api_p1', password='123')
        self.player2 = User.objects.create_user(username='api_p2', password='123')

        self.tasks = [
            Task.objects.create(
                subject='math',
                topic='algebra',
                difficulty='easy',
                text=f'task #{index}',
                correct_answer='42',
                hints=['h1', 'h2'],
            )
            for index in range(1, 3)
        ]

    def test_create_match_respects_requested_questions_count_even_if_tasks_are_few(self):
        self.client.force_authenticate(self.player1)

        response = self.client.post(
            reverse('create-match'),
            {
                'subject': 'math',
                'difficulty': 'easy',
                'questions_count': 5,
                'timer_enabled': True,
                'hints_enabled': True,
                'random_order': False,
                'is_private': False,
            },
            format='json',
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['questions_count'], 5)
        self.assertEqual(response.data['timer_enabled'], True)
        self.assertEqual(response.data['hints_enabled'], True)
        self.assertEqual(response.data['random_order'], False)

        match = Match.objects.get(id=response.data['match_id'])
        self.assertEqual(match.questions_count, 5)
        self.assertEqual(len(match.question_task_ids), 5)
        self.assertEqual(match.question_task_ids[0], self.tasks[0].id)
        self.assertEqual(match.question_task_ids[1], self.tasks[1].id)
        self.assertEqual(match.question_task_ids[2], self.tasks[0].id)

    def test_private_match_requires_token_to_join(self):
        self.client.force_authenticate(self.player1)
        create_response = self.client.post(
            reverse('create-match'),
            {
                'subject': 'math',
                'difficulty': 'easy',
                'questions_count': 2,
                'is_private': True,
            },
            format='json',
        )
        self.assertEqual(create_response.status_code, 201)
        match_id = create_response.data['match_id']
        token = create_response.data['private_token']

        self.client.force_authenticate(self.player2)
        no_token_join = self.client.post(reverse('join-match', kwargs={'match_id': match_id}), {}, format='json')
        self.assertEqual(no_token_join.status_code, 403)

        with_token_join = self.client.post(
            reverse('join-match', kwargs={'match_id': match_id}),
            {'token': token},
            format='json',
        )
        self.assertEqual(with_token_join.status_code, 200)
        self.assertEqual(with_token_join.data['status'], 'active')
>>>>>>> Stashed changes
