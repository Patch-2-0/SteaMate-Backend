from django.urls import path
from .views import CommunityAPIView, CommunityDetailAPIView

urlpatterns = [
    path('', CommunityAPIView.as_view()),
    path('<int:post_id>/', CommunityDetailAPIView.as_view()),
]   