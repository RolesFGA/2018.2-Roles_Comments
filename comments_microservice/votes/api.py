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


class VoteQueryset(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    filter_backends = (filters.OrderingFilter, filters.SearchFilter)

    def get_serializer_class(self):
        if self.action in ["retrieve", "list", "update", "create"]:
            return self.serializer_class

        return self.serializer_class

    @list_route(methods=["POST", "GET"])
    def up(self, request):
        """
        Adds a new vote to the object.
        :param: model, id, vote i.e. model=movies&id=359&vote=true
        :vote=option[True for up-vote, False for down-vote, None for no-vote]
        """
        user = request.user

        vote_param = request.query_params.get("vote", None)
        vote_dict = {"true": True,
                     "false": False}
        try:
            vote = vote_dict[vote_param]
            app_label = request.query_params.get("app_label", None)
            model = request.query_params.get("model", None)
            id = request.query_params.get("id", None)

            content_type = ContentType.objects.get( model=model)
            instance = content_type.get_object_for_this_type(pk=id)
            instance.votes.up(user, vote)
            message = "Successfully voted"

        except KeyError:
            message = "Please provide a like or dislike parameter."
        return Response({'message': message})

    @list_route(methods=["POST", "GET"])
    def down(self, request):
        """
        Removes vote to the object.
        :param: model, id i.e. model=movies&id=359
        """
        user = request.user
        app_label = request.query_params.get("app_label", None)
        model = request.query_params.get("model")
        id = request.query_params.get("id")
        content_type = ContentType.objects.get( model=model)
        instance = content_type.get_object_for_this_type(pk=id)

        instance.votes.down(user)
        return Response({'message': 'Successfully un-voted'})

    @list_route(methods=["GET"])
    def exists(self, request):
        """
        Check whether an object is already voted.
        :param: model, id i.e. model=movies&id=359
        """
        user = request.user
        app_label = request.query_params.get("app_label", None)
        model = request.query_params.get("model")
        id = request.query_params.get("id")
        content_type = ContentType.objects.get( model=model)
        instance = content_type.get_object_for_this_type(pk=id)

        voted = instance.votes.exists(user)

        return Response({'voted': voted})

    @list_route(methods=["GET"])
    def all(self, request):
        """
        Return all instances voted by user.
        :param: model, id i.e. model=movies&id=359
        """
        user = request.user
        app_label = request.query_params.get("app_label", None)
        model = request.query_params.get("model")
        id = request.query_params.get("id")
        content_type = ContentType.objects.get( model=model)
        instance = content_type.get_object_for_this_type(pk=id)
        all_instances = instance.votes.all(user).values()

        return Response(all_instances)

    @list_route(methods=["GET"])
    def count(self, request):
        """
        Returns the number of votes for the object.
        :param: model, id i.e. model=movies&id=359
        """

        app_label = request.query_params.get("app_label", None)
        model = request.query_params.get("model")
        id = request.query_params.get("id")
        content_type = ContentType.objects.get( model=model)
        instance = content_type.get_object_for_this_type(pk=id)
        vote_count = {'vote_count': instance.votes.count()}

        return Response(vote_count)

    @list_route(methods=["GET"])
    def users(self, request):
        """
        Returns a list of users who voted and their voting date.
        :param: model, id i.e. model=movies&id=359
        """

        app_label = request.query_params.get("app_label", None)
        model = request.query_params.get("model")
        id = request.query_params.get("id")
        content_type = ContentType.objects.get( model=model)
        instance = content_type.get_object_for_this_type(pk=id)
        users_count = {'users_count': instance.votes.users()}

        return Response(users_count)

    @list_route(methods=["GET"])
    def likes(self, request):
        """
        Returns the number of likes and dislikes for the object.
        :param: model, id i.e. model=movies&id=359
        """

        app_label = request.query_params.get("app_label", None)
        model = request.query_params.get("model")
        id = request.query_params.get("id")
        content_type = ContentType.objects.get( model=model)
        instance = content_type.get_object_for_this_type(pk=id)
        votes = instance.votes.likes()
        results = Counter(votes)

        return Response(results)
