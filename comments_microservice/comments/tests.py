from django.test import TestCase
from .models import Comment
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse, resolve


class ModelTestCase(TestCase):
    def setUp(self):
        """Define the test client and other test variables."""
        self.authorName = "Fulano"
        self.authorID = 1
        self.text = "O comentario vem aqui."
        self.comment = Comment(authorName=self.authorName,
                               authorID=self.authorID,
                               text=self.text,
                               eventID=1,)

    def test_model_can_create_a_comment(self):
        """Test the comment model can create a comment."""
        old_count = Comment.objects.count()
        self.comment.save()
        new_count = Comment.objects.count()
        self.assertNotEqual(old_count, new_count)


class ViewTestCase(TestCase):
    """Test suite for the api views."""

    def setUp(self):
        """Define the test client and other test variables."""
        user = User.objects.create(username="User01")
        self.client = APIClient()
        self.client.force_authenticate(user=user)
        self.comment_data = {'authorName': 'Fulano',
                             'authorID': 1,
                             'text': 'O comentario vem aqui',
                             'eventID': 1}
        self.response = self.client.post(
            reverse('comment-list'),
            self.comment_data,
            format='json')

    """ Test: Creating """

    def test_api_comment_create(self):
        """Test the api has bucket creation capability."""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    """ Test: Getting """

    def test_api_comment_get(self):
        """Test the api can get a given comment."""
        comment = Comment.objects.get()
        response = self.client.get(
            reverse('comment-detail',
            kwargs={'pk': comment.id}), format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, comment)

    """ Test: Updating """

    def test_api_comment_update(self):
        """Test the api can update a given comment."""
        comment = Comment.objects.get()
        change_comment = {'authorName': 'Fulano',
                          'authorID': 1,
                          'text': 'Novo comentário',
                          'eventID': 1}
        res = self.client.put(
            reverse('comment-detail', kwargs={'pk': comment.id}),
            change_comment, format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        """API cannot update if eventID is negative"""
        comment2 = Comment.objects.get()
        change_comment2 = {'authorName': 'Beltrano',
                           'eventID': -2,
                           'text': 'Comentário'}
        res = self.client.put(
            reverse('comment-detail', kwargs={'pk': comment2.id}),
            change_comment2, format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    """ DELETING """

    def test_api_can_delete_comment(self):

        """Test the api can delete a comment."""
        comment = Comment.objects.get()
        response = self.client.delete(
            reverse('comment-detail', kwargs={'pk': comment.id}),
            format='json',
            follow=True)

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
