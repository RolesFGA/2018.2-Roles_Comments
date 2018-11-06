
""" Serializers for api support on Votes app. """

# Core Django imports
from django.db import transaction

# Third party imports
from rest_framework import serializers

# Imports form Vote app
from .models import Vote


class VoteSerializer(serializers.ModelSerializer):

    """ Returns serialized data of Vote instances. """

    @transaction.atomic
    class Meta:
        model = Vote
        fields = '__all__'
