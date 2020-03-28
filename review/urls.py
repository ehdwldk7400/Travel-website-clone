from django.urls import path
from .views      import ReviewView, ReviewDetail

urlpatterns = [
    path('', ReviewView.as_view()),
    path('/<int:review_id>', ReviewDetail.as_view()),
]