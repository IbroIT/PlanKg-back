from django.urls import path
from .views import ReviewListView, ReviewCreateView, ReviewUpdateView, ReviewDeleteView, MyReviewView

urlpatterns = [
    path('reviews/', ReviewListView.as_view(), name='review-list'),
    path('reviews/<int:service_id>/', ReviewListView.as_view(), name='service-reviews'),
    path('reviews/create/', ReviewCreateView.as_view(), name='review-create'),
    path('reviews/my/<int:service_id>/', MyReviewView.as_view(), name='my-review'),
    path('reviews/<int:pk>/update/', ReviewUpdateView.as_view(), name='review-update'),
    path('reviews/<int:pk>/delete/', ReviewDeleteView.as_view(), name='review-delete'),
]
