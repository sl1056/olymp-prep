from django.contrib.auth.models import User
from django.test import TestCase

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
