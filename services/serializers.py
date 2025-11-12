from rest_framework import serializers
from .models import Category, Service, Favorite
from users.serializers import UserSerializer


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    subcategories = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'icon', 'translations', 'parent', 'subcategories', 'order']
    
    def get_name(self, obj):
        lang = self.context.get('lang', 'ru')
        return obj.get_translation(lang)
    
    def get_subcategories(self, obj):
        if obj.parent is None:  # Only for parent categories
            subcats = obj.subcategories.all()
            return CategorySerializer(subcats, many=True, context=self.context).data
        return []


class ServiceListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    
    class Meta:
        model = Service
        fields = ['id', 'user', 'category', 'title', 'description', 'price', 
                  'price_type', 'status', 'city', 'district', 'image', 'logo', 
                  'rating', 'reviews_count', 'views_count', 'capacity', 
                  'hourly_rate', 'gender', 'is_favorited', 'created_at']
    
    def get_title(self, obj):
        lang = self.context.get('lang', 'ru')
        trans = obj.get_translation(lang)
        return trans.get('title', '')
    
    def get_description(self, obj):
        lang = self.context.get('lang', 'ru')
        trans = obj.get_translation(lang)
        desc = trans.get('description', '')
        return desc[:200] + '...' if len(desc) > 200 else desc
    
    def get_image(self, obj):
        if obj.logo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.logo.url)
        elif obj.image1:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image1.url)
        return None
    
    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Favorite.objects.filter(user=request.user, service=obj).exists()
        return False


class ServiceDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    videos = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    
    class Meta:
        model = Service
        fields = ['id', 'user', 'category', 'title', 'description', 'price', 
                  'price_type', 'status', 'city', 'district', 'phone', 'email', 
                  'website', 'instagram', 'facebook', 'logo', 'capacity', 
                  'average_check', 'event_duration', 'additional_services',
                  'experience_years', 'hourly_rate', 'gender', 'images', 'videos',
                  'rating', 'reviews_count', 'views_count', 'is_favorited',
                  'created_at', 'updated_at']
    
    def get_title(self, obj):
        lang = self.context.get('lang', 'ru')
        trans = obj.get_translation(lang)
        return trans.get('title', '')
    
    def get_description(self, obj):
        lang = self.context.get('lang', 'ru')
        trans = obj.get_translation(lang)
        return trans.get('description', '')
    
    def get_images(self, obj):
        request = self.context.get('request')
        images = []
        for img_field in [obj.image1, obj.image2, obj.image3, obj.image4, obj.image5]:
            if img_field:
                images.append(request.build_absolute_uri(img_field.url) if request else img_field.url)
        return images
    
    def get_videos(self, obj):
        request = self.context.get('request')
        videos = []
        for vid_field in [obj.video1, obj.video2]:
            if vid_field:
                videos.append(request.build_absolute_uri(vid_field.url) if request else vid_field.url)
        return videos
    
    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Favorite.objects.filter(user=request.user, service=obj).exists()
        return False


class ServiceCreateUpdateSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Service
        fields = ['id', 'category_id', 'translations', 'price', 'price_type',
                  'city', 'district', 'phone', 'email', 'website', 'instagram', 
                  'facebook', 'logo', 'capacity', 'average_check', 'event_duration',
                  'additional_services', 'experience_years', 'hourly_rate', 'gender',
                  'image1', 'image2', 'image3', 'image4', 'image5', 'video1', 'video2']
    
    def validate_translations(self, value):
        required_langs = ['ru', 'en', 'kg']
        for lang in required_langs:
            if lang not in value:
                raise serializers.ValidationError(f"Translation for '{lang}' is required")
            if 'title' not in value[lang] or 'description' not in value[lang]:
                raise serializers.ValidationError(f"Title and description required for '{lang}'")
        return value
    
    def create(self, validated_data):
        category_id = validated_data.pop('category_id')
        validated_data['category_id'] = category_id
        validated_data['user'] = self.context['request'].user
        validated_data['status'] = 'pending'  # All new services start as pending
        return super().create(validated_data)


class FavoriteSerializer(serializers.ModelSerializer):
    service = ServiceListSerializer(read_only=True)
    
    class Meta:
        model = Favorite
        fields = ['id', 'service', 'created_at']
