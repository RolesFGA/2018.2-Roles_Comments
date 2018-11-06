__author__ = 'consultadd66'

import sys
sys.path.append("..")

from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from ..models import Vote
from rest_framework.reverse import reverse
from comments.models import Comment
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from rest_framework.test import APIClient


class CreateVoteTest(APITestCase):
    def setUp(self):
        user = User.objects.create(username="User01")
        self.client = APIClient()
        self.client.force_authenticate(user=user)
        self.content_type = ContentType.objects.get(model="comment")
        self.data = {'content_type': self.content_type.id, 'object_id': 1, 'user': user.id}

    def test_can_create_vote(self):
        response = self.client.post(reverse('vote-list'), self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ReadVoteTest(APITestCase):
    def setUp(self):
        user = User.objects.create(username="User01")
        self.client = APIClient()
        self.client.force_authenticate(user=user)
        self.content_type = ContentType.objects.get(model="comment")
        self.vote = Vote.objects.create(content_type_id=1, object_id=1, user_id=1)

    def test_can_read_vote_list(self):
        response = self.client.get(reverse('vote-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_read_vote_detail(self):
        response = self.client.get(reverse('vote-detail', args=[self.vote.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UpdateVoteTest(APITestCase):
    def setUp(self):
        user = User.objects.create(username="User01")
        self.client = APIClient()
        self.client.force_authenticate(user=user)
        self.content_type = ContentType.objects.get(model="comment")
        self.data = {'content_type': self.content_type.id, 'object_id': 1, 'user': user.id}
        self.vote = Vote.objects.create(content_type_id=1, object_id=1, user_id=1)

    def test_can_update_vote(self):
        response = self.client.put(reverse('vote-detail', args=[self.vote.id]), self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DeleteVoteTest(APITestCase):
    def setUp(self):
        user = User.objects.create(username="User01")
        self.client = APIClient()
        self.client.force_authenticate(user=user)
        self.content_type = ContentType.objects.get(model="comment")
        self.vote = Vote.objects.create(content_type_id=1, object_id=1, user_id=1)

    def test_can_delete_vote(self):
        response = self.client.delete(reverse('vote-detail', args=[self.vote.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class VoteQuerysetTest(APITestCase):
    def setUp(self):
        user = User.objects.create(username="User01")
        self.client = APIClient()
        self.client.force_authenticate(user=user)

        self.comment = Comment.objects.create(author=user,
                                              text= "O COMENTARIO VEM AQUI")

    def test_up(self):
        # user should be login to vote

        response = self.client.get(reverse('vote-list') + 'up/', {'model': 'comment', 'id': str(self.comment.id), 'vote': 'true'})
        assert response.status_code == 200
        assert response.data['message'] == 'Successfully voted'

        response = self.client.get(reverse('vote-list') + 'up/', {'model': 'comment', 'id': str(self.comment.id)})
        assert response.data['message'] == "Please provide a like or dislike parameter."

    def test_up_post(self):
        # user should be login to vote

        response = self.client.post(reverse('vote-list') + 'up/?model=comment&id='+str(self.comment.id)+'&vote=true', content_type="application/json")
        assert response.status_code == 200
        assert response.data['message'] == 'Successfully voted'

    def test_down(self):
        # user should be login to down vote

        response = self.client.get(reverse('vote-list') + 'down/', {'model': 'comment', 'id': str(self.comment.id)})
        assert response.status_code == 200
        assert response.data['message'] == 'Successfully un-voted'

    def test_down_post(self):
        # user should be login to down vote

        response = self.client.post(reverse('vote-list') + 'down/?model=comment&id='+str(self.comment.id), content_type="application/json")
        assert response.status_code == 200
        assert response.data['message'] == 'Successfully un-voted'

    def test_exists(self):
        response = self.client.get(reverse('vote-list') + 'exists/', {'model': 'comment', 'id': str(self.comment.id)})
        assert response.status_code == 200
        assert response.data

    def test_all(self):
        # check after up-vote
        self.client.get(reverse('vote-list') + 'up/?model=comment&id='+str(self.comment.id)+'&vote=true')
        response = self.client.get(reverse('vote-list') + 'all/?model=comment&id='+str(self.comment.id))
        assert response.status_code == 200
        assert response.data

        # check after down-vote
        self.client.get(reverse('vote-list') + 'down/', {'model': 'comment', 'id': str(self.comment.id)})
        response = self.client.get(reverse('vote-list') + 'all/', {'model': 'comment', 'id': str(self.comment.id)})
        assert response.status_code == 200
        assert len(response.data) == 0

    def test_count(self):
        # check before vote
        response = self.client.get(reverse('vote-list') + 'count/', {'model': 'comment', 'id': str(self.comment.id)})
        assert response.status_code == 200
        self.assertDictEqual(response.data, {'vote_count': 0})

        # check after vote
        self.client.get(reverse('vote-list') + 'up/', {'model': 'comment', 'id': str(self.comment.id), 'vote': 'true'})
        response = self.client.get(reverse('vote-list') + 'count/', {'model': 'comment', 'id': str(self.comment.id)})
        assert response.status_code == 200
        self.assertDictEqual(response.data, {'vote_count': 1})

    def test_users(self):
        response = self.client.get(reverse('vote-list') + 'users/', {'model': 'comment', 'id': str(self.comment.id)})
        assert response.status_code == 200

    def test_likes(self):
        response = self.client.get(reverse('vote-list') + 'likes/?model=comment&id='+str(self.comment.id))
        assert response.status_code == 200
