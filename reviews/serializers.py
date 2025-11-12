from rest_framework import serializers
from .models import Review
from users.serializers import UserSerializer


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'user', 'service', 'rating', 'comment', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['service', 'rating', 'comment']
    
    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Рейтинг должен быть от 1 до 5")
        return value
    
    def validate_service(self, value):
        if not value:
            raise serializers.ValidationError("Необходимо указать услугу")
        return value
    
    def validate_comment(self, value):
        if not value or len(value.strip()) < 10:
            raise serializers.ValidationError("Комментарий должен содержать минимум 10 символов")
        return value
    
    def validate(self, attrs):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("Вы должны быть авторизованы для оставления отзыва")
        
        user = request.user
        service = attrs.get('service')
        
        # Проверяем, есть ли уже отзыв от этого пользователя на эту услугу
        if Review.objects.filter(user=user, service=service).exists():
            raise serializers.ValidationError(
                "Вы уже оставили отзыв на эту услугу. Вы можете отредактировать существующий отзыв."
            )
        
        return attrs
    
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)
