from django.urls import path
from .views import (CategoryListView, ServiceListView, ServiceDetailView,
                    ServiceCreateView, ServiceUpdateView, ServiceDeleteView, 
                    MyServicesView, FavoriteListView, FavoriteToggleView)

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('services/', ServiceListView.as_view(), name='service-list'),
    path('services/<int:pk>/', ServiceDetailView.as_view(), name='service-detail'),
    path('services/create/', ServiceCreateView.as_view(), name='service-create'),
    path('services/<int:pk>/update/', ServiceUpdateView.as_view(), name='service-update'),
    path('services/<int:pk>/delete/', ServiceDeleteView.as_view(), name='service-delete'),
    path('services/my/', MyServicesView.as_view(), name='my-services'),
    path('favorites/', FavoriteListView.as_view(), name='favorite-list'),
    path('favorites/toggle/<int:service_id>/', FavoriteToggleView.as_view(), name='favorite-toggle'),
]
