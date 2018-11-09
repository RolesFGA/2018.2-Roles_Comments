from __future__ import absolute_import, unicode_literals

from rest_framework.routers import DefaultRouter

from .api import VoteQueryset

router = DefaultRouter()
router.register(r'votes', VoteQueryset)

urlpatterns = router.urls
