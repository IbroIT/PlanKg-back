from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Review
from .serializers import ReviewSerializer, ReviewCreateSerializer


class ReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None  # Отключаем пагинацию
    
    def get_queryset(self):
        service_id = self.kwargs.get('service_id')
        if service_id:
            return Review.objects.filter(service_id=service_id).select_related('user')
        return Review.objects.all().select_related('user', 'service')


class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def create(self, request, *args, **kwargs):
        print(f"Review create request - User: {request.user}, Data: {request.data}")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        review = serializer.save()
        
        # Возвращаем полные данные отзыва с информацией о пользователе
        output_serializer = ReviewSerializer(review)
        headers = self.get_success_headers(output_serializer.data)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        serializer.save()


class MyReviewView(generics.RetrieveAPIView):
    """Получить отзыв текущего пользователя на конкретную услугу"""
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        service_id = self.kwargs.get('service_id')
        try:
            return Review.objects.get(user=self.request.user, service_id=service_id)
        except Review.DoesNotExist:
            return None
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is None:
            return Response({'detail': 'Отзыв не найден'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ReviewUpdateView(generics.UpdateAPIView):
    serializer_class = ReviewCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)


class ReviewDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)
