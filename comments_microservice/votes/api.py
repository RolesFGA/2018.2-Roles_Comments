"""
APIs for votes against a model.
"""
from collections import Counter

# Core Django imports
from django.contrib.contenttypes.models import ContentType

# Third party imports
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.decorators import list_route
from rest_framework.response import Response

# Imports from local apps
from .models import Vote

from .serializers import VoteSerializer


def populate_instance(request):
    model = request.query_params.get("model")
    id = request.query_params.get("id")
    content_type = ContentType.objects.get(model=model)
    instance = content_type.get_object_for_this_type(pk=id)
    return instance


class VoteQueryset(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    filter_backends = (filters.OrderingFilter, filters.SearchFilter)

    def get_serializer_class(self):
        return self.serializer_class

    @list_route(methods=["POST", "GET"])
    def up(self, request):
        user = request.user

        vote_param = request.query_params.get("vote", None)
        vote_dict = {"true": True,
                     "false": False}
        try:
            vote = vote_dict[vote_param]
            instance = populate_instance(request)
            instance.votes.up(user, vote)
            message = "Successfully voted"

        except KeyError:
            message = "Please provide a like or dislike parameter."
        return Response({'message': message})

    @list_route(methods=["POST", "GET"])
    def down(self, request):
        user = request.user
        instance = populate_instance(request)
        instance.votes.down(user)
        return Response({'message': 'Successfully un-voted'})

    @list_route(methods=["GET"])
    def exists(self, request):
        user = request.user
        instance = populate_instance(request)
        voted = instance.votes.exists(user)

        return Response({'voted': voted})

    @list_route(methods=["GET"])
    def all(self, request):
        user = request.user
        instance = populate_instance(request)
        all_instances = instance.votes.all(user).values()

        return Response(all_instances)

    @list_route(methods=["GET"])
    def count(self, request): # Refatorar
        instance = populate_instance(request)
        vote_count = {'vote_count': instance.votes.count()}

        return Response(vote_count)

    @list_route(methods=["GET"])
    def users(self, request): # Refatorar
        instance = populate_instance(request)
        users_count = {'users_count': instance.votes.users()}

        return Response(users_count)

    @list_route(methods=["GET"])
    def likes(self, request):
        instance = populate_instance(request)
        votes = instance.votes.likes()
        results = Counter(votes)

        return Response(results)
