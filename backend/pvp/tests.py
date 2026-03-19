from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

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

    def test_non_participant_cannot_access_waiting_match_via_websocket(self):
        outsider = User.objects.create_user(username='outsider', password='123')
        waiting_match = Match.objects.create(
            player1=self.player1,
            status='waiting',
            task=self.task,
        )
        consumer = MatchConsumer()

        self.assertTrue(consumer._check_participation(waiting_match.id, self.player1.id))
        self.assertFalse(consumer._check_participation(waiting_match.id, outsider.id))

    def test_match_advances_to_next_question(self):
        second_task = Task.objects.create(
            subject='math',
            topic='algebra-2',
            difficulty='easy',
            text='5+5?',
            correct_answer='10',
        )
        self.match.task = self.task
        self.match.question_task_ids = [self.task.id, second_task.id]
        self.match.questions_count = 2
        self.match.current_question_index = 1
        self.match.save(update_fields=['task', 'question_task_ids', 'questions_count', 'current_question_index'])

        consumer_p1 = self._make_consumer(self.player1)
        consumer_p2 = self._make_consumer(self.player2)

        consumer_p1._save_answer_to_db('4')
        consumer_p2._save_answer_to_db('4')
        next_question = consumer_p1._advance_to_next_question(self.match.id)

        self.match.refresh_from_db()

        self.assertIsNotNone(next_question)
        self.assertEqual(self.match.current_question_index, 2)
        self.assertEqual(self.match.task_id, second_task.id)
        self.assertEqual(self.match.player1_answer, '')
        self.assertEqual(self.match.player2_answer, '')
        self.assertIsNone(self.match.player1_submitted_at)
        self.assertIsNone(self.match.player2_submitted_at)


class PvpViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.player1 = User.objects.create_user(username='v1', password='123')
        self.player2 = User.objects.create_user(username='v2', password='123')
        self.task = Task.objects.create(
            subject='math',
            topic='geometry',
            difficulty='easy',
            text='1+1?',
            correct_answer='2',
        )

    def test_status_endpoint_works_without_trailing_slash(self):
        match = Match.objects.create(
            player1=self.player1,
            player2=self.player2,
            status='active',
            task=self.task,
        )
        self.client.force_authenticate(user=self.player1)

        response = self.client.get(f'/api/pvp/status/{match.id}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['match_id'], match.id)
        self.assertEqual(response.data['status'], 'active')

    def test_join_is_idempotent_for_already_joined_second_player(self):
        match = Match.objects.create(
            player1=self.player1,
            player2=self.player2,
            status='active',
            task=self.task,
        )
        self.client.force_authenticate(user=self.player2)

        response = self.client.post(f'/api/pvp/join/{match.id}/', data={})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['match_id'], match.id)
        self.assertEqual(response.data['status'], 'active')

    def test_create_match_sets_current_question_index_default(self):
        self.client.force_authenticate(user=self.player1)

        response = self.client.post(
            '/api/pvp/create/',
            data={'subject': 'math', 'difficulty': 'easy'},
            format='json',
        )

        self.assertEqual(response.status_code, 201)
        match = Match.objects.get(id=response.data['match_id'])
        self.assertEqual(match.current_question_index, 1)
        self.assertEqual(match.questions_count, 1)
        self.assertEqual(match.player1_score, 0)
        self.assertEqual(match.player2_score, 0)
        self.assertEqual(match.question_task_ids, [self.task.id])

    def test_create_match_respects_custom_question_count(self):
        Task.objects.create(
            subject='math',
            topic='geometry-2',
            difficulty='easy',
            text='3+3?',
            correct_answer='6',
        )
        Task.objects.create(
            subject='math',
            topic='geometry-3',
            difficulty='easy',
            text='4+4?',
            correct_answer='8',
        )
        self.client.force_authenticate(user=self.player1)

        response = self.client.post(
            '/api/pvp/create/',
            data={'subject': 'math', 'difficulty': 'easy', 'question_count': 3},
            format='json',
        )

        self.assertEqual(response.status_code, 201)
        match = Match.objects.get(id=response.data['match_id'])
        self.assertEqual(match.questions_count, 3)
        self.assertEqual(len(match.question_task_ids), 3)
