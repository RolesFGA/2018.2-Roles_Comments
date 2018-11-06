from django.urls import path
from comments import views

urlpatterns = [
    path('', views.api_root),
    path('comment/', views.CommentList.as_view(), name='comment-list'),
    path('comment/<int:pk>/', views.CommentDetail.as_view(), name='comment-detail'),
]
