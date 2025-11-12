from rest_framework import generics, filters, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from .models import Category, Service, Favorite
from .serializers import (CategorySerializer, ServiceListSerializer, 
                          ServiceDetailSerializer, ServiceCreateUpdateSerializer,
                          FavoriteSerializer)


class CategoryListView(generics.ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None  # Disable pagination for categories
    
    def get_queryset(self):
        # Return only parent categories with their subcategories
        return Category.objects.filter(parent__isnull=True).prefetch_related('subcategories')
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['lang'] = self.request.query_params.get('lang', 'ru')
        return context


class ServiceListView(generics.ListAPIView):
    serializer_class = ServiceListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'rating', 'price', 'views_count']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = Service.objects.filter(
            is_active=True, 
            status='approved',
            category__isnull=False  # Показываем только услуги с категорией
        ).select_related('user', 'category')
        
        # Filters
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        city = self.request.query_params.get('city')
        if city:
            queryset = queryset.filter(city__icontains=city)
        
        # Capacity filter (for restaurants/venues)
        min_capacity = self.request.query_params.get('min_capacity')
        if min_capacity:
            queryset = queryset.filter(capacity__gte=min_capacity)
        
        max_capacity = self.request.query_params.get('max_capacity')
        if max_capacity:
            queryset = queryset.filter(capacity__lte=max_capacity)
        
        # Gender filter (for singers, dancers, etc.)
        gender = self.request.query_params.get('gender')
        if gender:
            queryset = queryset.filter(Q(gender=gender) | Q(gender='any'))
        
        min_price = self.request.query_params.get('min_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        
        max_price = self.request.query_params.get('max_price')
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        min_rating = self.request.query_params.get('min_rating')
        if min_rating:
            queryset = queryset.filter(rating__gte=min_rating)
        
        # Search
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(translations__ru__title__icontains=search) |
                Q(translations__ru__description__icontains=search) |
                Q(translations__en__title__icontains=search) |
                Q(translations__en__description__icontains=search) |
                Q(translations__kg__title__icontains=search) |
                Q(translations__kg__description__icontains=search) |
                Q(city__icontains=search)
            )
        
        return queryset
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['lang'] = self.request.query_params.get('lang', 'ru')
        return context


class ServiceDetailView(generics.RetrieveAPIView):
    queryset = Service.objects.filter(is_active=True)
    serializer_class = ServiceDetailSerializer
    permission_classes = [permissions.AllowAny]
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment views count
        instance.views_count += 1
        instance.save(update_fields=['views_count'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['lang'] = self.request.query_params.get('lang', 'ru')
        return context


class ServiceCreateView(generics.CreateAPIView):
    serializer_class = ServiceCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]


class ServiceUpdateView(generics.UpdateAPIView):
    serializer_class = ServiceCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Service.objects.filter(user=self.request.user)


class ServiceDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Service.objects.filter(user=self.request.user)


class MyServicesView(generics.ListAPIView):
    serializer_class = ServiceListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Service.objects.filter(user=self.request.user).select_related('category')
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['lang'] = self.request.query_params.get('lang', 'ru')
        return context


class FavoriteListView(generics.ListAPIView):
    """Get user's favorite services"""
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).select_related('service', 'service__category', 'service__user')
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['lang'] = self.request.query_params.get('lang', 'ru')
        return context


class FavoriteToggleView(APIView):
    """Add or remove service from favorites"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, service_id):
        try:
            service = Service.objects.get(id=service_id, is_active=True)
        except Service.DoesNotExist:
            return Response({'error': 'Service not found'}, status=status.HTTP_404_NOT_FOUND)
        
        favorite, created = Favorite.objects.get_or_create(user=request.user, service=service)
        
        if not created:
            # Already favorited, so remove it
            favorite.delete()
            return Response({'status': 'removed', 'is_favorited': False}, status=status.HTTP_200_OK)
        
        return Response({'status': 'added', 'is_favorited': True}, status=status.HTTP_201_CREATED)
