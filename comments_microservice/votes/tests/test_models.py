__author__ = 'consultadd66'
from django.test import TestCase
from ..models import Vote


class TestVote(TestCase):

    def setUp(self):
        self.vote = Vote()

    def test_vote(self):
        self.assertIsInstance(self.vote, Vote)
