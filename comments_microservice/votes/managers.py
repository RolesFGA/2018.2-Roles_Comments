from collections import defaultdict
from django.db import models, transaction
from django.db.models import Count, F
from django.db.models.query import QuerySet
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation

from .models import Vote
from .utils import instance_required


class VotedQuerySet(QuerySet):
    """
    if call votes.annotate with an `user` argument then add `is_voted` to each instance
    """

    def __init__(self, model=None, query=None, using=None, user=None):
        self.user = user
        super(VotedQuerySet, self).__init__(model=model, query=query, using=using)

    def __iter__(self):
        super(VotedQuerySet, self).__iter__()
        if self.user is None:
            return iter(self._result_cache)

        objects = self._result_cache
        user_id = self.user.id
        contenttype = ContentType.objects.get_for_model(self.model)
        object_ids = [r.id for r in objects]

        voted_users = defaultdict(list)
        votes = Vote.objects.filter(content_type=contenttype, object_id__in=object_ids)
        for v in votes:
            voted_users[v.object_id].append(v.user_id)

        for r in objects:
            r.is_voted = user_id in voted_users.get(r.id, [])

        self._result_cache = objects
        return iter(objects)


class _VotableManager(models.Manager):
    def __init__(self, through, model, instance, field_name='votes'):
        self.through = through
        self.model = model
        self.instance = instance
        self.field_name = field_name


    @instance_required
    def up(self, user, vote):
        with transaction.atomic():
            if self.through.objects.filter(user=user, content_object=self.instance).exists():
                c_type = ContentType.objects.get_for_model(self.instance)
                vote_obj = self.through.objects.get(user=user, object_id=self.instance.id, content_type=c_type)
                vote_obj.vote = vote
                vote_obj.save()
                self.instance.save()
            else:
                self.through(user=user, content_object=self.instance, vote=vote).save()


    @instance_required
    def down(self, user):
        with transaction.atomic():
            self.through.objects.filter(user=user, content_object=self.instance).delete()


    @instance_required
    def exists(self, user):
        return self.through.objects.filter(user=user, content_object=self.instance).exists()

    def all(self, user):
        content_type = ContentType.objects.get_for_model(self.model)
        object_ids = self.through.objects.filter(user=user, content_type=content_type).values_list('object_id', flat=True)
        return self.model.objects.filter(pk__in=list(object_ids))

    def count(self, vote = None):
        if vote is None:
            return self.through.votes_for(self.model, self.instance).count()
        else:
            return self.through.votes_for(self.model, self.instance).filter(vote = vote).count()

    def likes(self):
        return self.through.votes_for(self.model, self.instance).values_list("vote", flat=True)

    def users(self):
        return self.through.votes_for(self.model, self.instance).order_by('-create_at').values_list('user_id', 'create_at')

    def annotate(self, queryset=None, user=None, annotation='num_votes', reverse=True):
        order = reverse and '-%s' % annotation or annotation
        kwargs = {annotation:Count('%s__user' % self.field_name)}
        queryset = queryset if queryset is not None else self.model.objects.all()
        queryset = queryset.annotate(**kwargs).order_by(order, '-id')
        return VotedQuerySet(model=queryset.model, query=queryset.query, user=user)


class VotableManager(GenericRelation):
    def __init__(self, through=Vote, manager=_VotableManager, **kwargs):
        self.through = through
        self.manager = manager
        kwargs['verbose_name'] = kwargs.get('verbose_name', _('Votes'))

        super(VotableManager, self).__init__(self.through, **kwargs)

    def __get__(self, instance, model):
        if instance is not None and instance.pk is None:
            raise ValueError("%s objects need to have a primary key value "
                "before you can access their votes." % model.__name__)
        manager = self.manager(
            through=self.through,
            model=model,
            instance=instance,
            field_name=self.name,
            
        )
        return manager

    def contribute_to_class(self, cls, name):
        super(VotableManager, self).contribute_to_class(cls, name)
        setattr(cls, name, self)
