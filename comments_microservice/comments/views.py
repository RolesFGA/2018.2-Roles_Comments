from rest_framework import generics
from .models import Comment
from .serializers import CommentSerializer
from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'comments': reverse('comment-list', request=request, format=format)
    })


class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    def get_queryset(self):
        queryset = Comment.objects.all()
        eventID = self.request.query_params.get('eventID', None)
        if eventID is not None:
            queryset = queryset.filter(eventID=eventID)
        return queryset


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
