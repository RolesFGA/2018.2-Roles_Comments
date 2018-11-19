from django.db import models
from votes.managers import VotableManager
from django.core.exceptions import ValidationError


def not_negative(eventId):
    if eventId < 0:
        raise ValidationError('Numero não pode ser negativo')


class Comment(models.Model):
    author = models.CharField(max_length=150)
    text = models.CharField(max_length=128)
    answerId = models.IntegerField(default=0)
    eventId = models.IntegerField(validators=[not_negative])
    created = models.DateTimeField(auto_now=False, null=True)
    edited = models.DateTimeField(auto_now=False, null=True)
    votes = VotableManager()

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return str(self.id)
