from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    translations = models.JSONField(default=dict, help_text='{"ru": "Название", "en": "Name", "kg": "Аталышы"}')
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def get_translation(self, lang='ru'):
        return self.translations.get(lang, self.translations.get('ru', 'No name'))
    
    def __str__(self):
        return self.get_translation('ru')
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['order', 'slug']


class Service(models.Model):
    PRICE_TYPE_CHOICES = (
        ('fixed', 'Fixed Price'),
        ('negotiable', 'Negotiable'),
        ('hourly', 'Hourly Rate'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'На рассмотрении'),
        ('approved', 'Одобрено'),
        ('rejected', 'Отклонено'),
    )
    
    GENDER_CHOICES = (
        ('male', 'Мужчина'),
        ('female', 'Женщина'),
        ('any', 'Не важно'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='services')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='services')
    
    # Multilingual fields
    translations = models.JSONField(default=dict, help_text='{"ru": {"title": "...", "description": "..."}, ...}')
    
    # Common fields
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_type = models.CharField(max_length=20, choices=PRICE_TYPE_CHOICES, default='fixed')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100, blank=True)
    
    # Contact info
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    instagram = models.CharField(max_length=100, blank=True)
    facebook = models.CharField(max_length=100, blank=True)
    
    # For restaurants/venues
    logo = models.ImageField(upload_to='services/logos/', blank=True, null=True)
    capacity = models.IntegerField(null=True, blank=True, help_text='Вместимость (количество человек)')
    average_check = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text='Средний чек за вместимость')
    event_duration = models.CharField(max_length=100, blank=True, help_text='Длительность мероприятия')
    additional_services = models.JSONField(default=dict, blank=True, help_text='Дополнительные услуги')
    
    # For individual providers (photographers, entertainers, etc)
    experience_years = models.IntegerField(null=True, blank=True, help_text='Опыт работы (лет)')
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text='Стоимость за час')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='any', blank=True)
    
    # Media
    image1 = models.ImageField(upload_to='services/', blank=True, null=True)
    image2 = models.ImageField(upload_to='services/', blank=True, null=True)
    image3 = models.ImageField(upload_to='services/', blank=True, null=True)
    image4 = models.ImageField(upload_to='services/', blank=True, null=True)
    image5 = models.ImageField(upload_to='services/', blank=True, null=True)
    video1 = models.FileField(upload_to='services/videos/', blank=True, null=True)
    video2 = models.FileField(upload_to='services/videos/', blank=True, null=True)
    
    views_count = models.IntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    reviews_count = models.IntegerField(default=0)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_translation(self, lang='ru'):
        return self.translations.get(lang, self.translations.get('ru', {}))
    
    def update_rating(self):
        """Update average rating from reviews"""
        from reviews.models import Review
        reviews = Review.objects.filter(service=self)
        if reviews.exists():
            self.rating = reviews.aggregate(models.Avg('rating'))['rating__avg']
            self.reviews_count = reviews.count()
            self.save(update_fields=['rating', 'reviews_count'])
        
    def __str__(self):
        trans = self.get_translation('ru')
        return trans.get('title', 'Untitled Service')
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['category', '-created_at']),
            models.Index(fields=['city', '-created_at']),
            models.Index(fields=['status', '-created_at']),
        ]


class Favorite(models.Model):
    """User's favorite services (likes)"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'service']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} likes {self.service}"
