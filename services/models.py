from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions

User = get_user_model()


def validate_icon_file(value):
    """Validate icon file - allow GIF and other image formats, max size 5MB"""
    if value:
        # Check file size (5MB max)
        if value.size > 5 * 1024 * 1024:
            raise ValidationError('Icon file size cannot exceed 5MB.')
        
        # Check file extension
        valid_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp']
        if not any(str(value.name).lower().endswith(ext) for ext in valid_extensions):
            raise ValidationError('Icon must be a valid image file (PNG, JPG, GIF, SVG, WebP).')


class Category(models.Model):
    translations = models.JSONField(default=dict, help_text='{"ru": "Название", "en": "Name", "kg": "Аталышы"}')
    slug = models.SlugField(unique=True)
    icon = models.ImageField(
        upload_to='categories/icons/',
        blank=True,
        null=True,
        validators=[validate_icon_file],
        help_text='Icon image for the category'
    )
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
    
    # Search optimization field
    search_text = models.TextField(blank=True, help_text='Combined searchable text from titles and descriptions')
    
    # Common fields
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_type = models.CharField(max_length=20, choices=PRICE_TYPE_CHOICES, default='fixed')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    city = models.CharField(max_length=100)
    
    # Venue capacity (for restaurants/venues)
    capacity = models.IntegerField(null=True, blank=True, help_text='Venue capacity')
    
    # Additional common fields
    average_check = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text='Average check')
    event_duration = models.IntegerField(null=True, blank=True, help_text='Event duration in hours')
    additional_services = models.TextField(blank=True, help_text='Additional services offered')
    experience_years = models.IntegerField(null=True, blank=True, help_text='Years of experience')
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text='Hourly rate')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='any', blank=True, help_text='Gender preference')
    
    # Contact info
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    instagram = models.CharField(max_length=100, blank=True)
    facebook = models.CharField(max_length=100, blank=True)
    whatsapp = models.CharField(max_length=100, blank=True, help_text='WhatsApp username or phone number')
    telegram = models.CharField(max_length=100, blank=True, help_text='Telegram username')
    
    # Additional fields for specific categories
    additional_fields = models.JSONField(default=dict, blank=True, help_text='Additional fields specific to the category')
    
    # Equipment rental fields
    equipment_type = models.CharField(max_length=100, blank=True, help_text='Type of equipment for rental')
    rental_duration = models.CharField(max_length=50, blank=True, help_text='Rental duration (day, week, etc.)')
    rental_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text='Rental price')
    
    # Transport fields
    vehicle_type = models.CharField(max_length=100, blank=True, help_text='Type of vehicle')
    vehicle_capacity = models.IntegerField(null=True, blank=True, help_text='Vehicle capacity')
    driver_included = models.BooleanField(default=False, help_text='Driver included')
    decoration_available = models.BooleanField(default=False, help_text='Vehicle decoration available')
    
    # Food service fields
    cuisine_type = models.CharField(max_length=100, blank=True, help_text='Type of cuisine')
    service_type = models.CharField(max_length=50, choices=[('buffet', 'Buffet'), ('banquet', 'Banquet'), ('individual', 'Individual')], default='buffet', blank=True)
    minimum_order = models.IntegerField(null=True, blank=True, help_text='Minimum order quantity')
    delivery_included = models.BooleanField(default=False, help_text='Delivery included')
    staff_included = models.BooleanField(default=False, help_text='Staff included')
    
    # Beauty services fields
    service_duration = models.IntegerField(null=True, blank=True, help_text='Service duration in minutes')
    home_visit = models.BooleanField(default=False, help_text='Home visit available')
    
    # Security fields
    license_number = models.CharField(max_length=100, blank=True, help_text='License number')
    guard_count = models.IntegerField(null=True, blank=True, help_text='Number of guards')
    
    # Animation fields
    character_type = models.CharField(max_length=100, blank=True, help_text='Type of characters/animations')
    show_duration = models.IntegerField(null=True, blank=True, help_text='Show duration in minutes')
    props_included = models.BooleanField(default=False, help_text='Props included')
    
    # Technical equipment fields
    lighting_type = models.CharField(max_length=100, blank=True, help_text='Type of lighting')
    sound_system = models.CharField(max_length=100, blank=True, help_text='Sound system type')
    stage_setup = models.BooleanField(default=False, help_text='Stage setup included')
    
    # Photo/Video specific fields
    shooting_hour_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text='Price per shooting hour')
    full_day_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text='Full day shooting price')
    love_story_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text='Love story shooting price')
    portfolio_photos_count = models.IntegerField(null=True, blank=True, help_text='Number of photos in portfolio')
    delivery_time_days = models.IntegerField(null=True, blank=True, help_text='Delivery time in days')
    shooting_style = models.CharField(max_length=100, blank=True, help_text='Shooting style (reportage, studio, etc.)')
    second_operator = models.BooleanField(default=False, help_text='Second operator available')
    drone_available = models.BooleanField(default=False, help_text='Drone shooting available')
    video_format = models.CharField(max_length=50, choices=[('hd', 'HD'), ('4k', '4K'), ('full_hd', 'Full HD')], default='hd', blank=True)
    sound_recording = models.BooleanField(default=False, help_text='Sound recording included')
    montage_included = models.BooleanField(default=False, help_text='Video montage included')
    
    # Host/MC fields
    video_presentation = models.URLField(blank=True, help_text='Link to video presentation')
    languages = models.CharField(max_length=200, blank=True, help_text='Languages spoken')
    dress_code = models.CharField(max_length=100, blank=True, help_text='Dress code')
    time_limit = models.CharField(max_length=50, blank=True, help_text='Time limit for performance')
    
    # Venue fields
    stage_available = models.BooleanField(default=False, help_text='Stage available')
    sound_available = models.BooleanField(default=False, help_text='Sound system available')
    parking_available = models.BooleanField(default=False, help_text='Parking available')
    projector_available = models.BooleanField(default=False, help_text='Projector available')
    decor_available = models.BooleanField(default=False, help_text='Decor available')
    menu_available = models.BooleanField(default=False, help_text='Menu available')
    working_hours = models.CharField(max_length=100, blank=True, help_text='Working hours')
    
    # Music fields
    music_genre = models.CharField(max_length=100, blank=True, help_text='Music genre')
    equipment_provided = models.BooleanField(default=False, help_text='Equipment provided')
    repertoire = models.TextField(blank=True, help_text='Repertoire description')
    performance_type = models.CharField(max_length=50, choices=[('live', 'Live'), ('dj', 'DJ'), ('backing_track', 'Backing Track')], default='live', blank=True)
    
    # Artist/Show fields
    show_type = models.CharField(max_length=100, blank=True, help_text='Type of show/performance')
    performance_video = models.URLField(blank=True, help_text='Link to performance video')
    stage_requirements = models.TextField(blank=True, help_text='Stage requirements')
    
    # Bakery/Cake fields
    cake_weight_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text='Cake weight in kg')
    flavors_available = models.TextField(blank=True, help_text='Available flavors')
    advance_order_days = models.IntegerField(null=True, blank=True, help_text='Advance order required (days)')
    
    # Waiter/Staff fields
    staff_count = models.IntegerField(null=True, blank=True, help_text='Number of staff members')
    uniform_provided = models.BooleanField(default=False, help_text='Uniform provided')
    
    # Florist/Decorator fields
    services_offered = models.TextField(blank=True, help_text='Services offered (arches, tables, photo zones, etc.)')
    wedding_decor_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text='Average wedding decor price')
    custom_calculation = models.BooleanField(default=False, help_text='Custom price calculation available')
    
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
    
    def update_search_text(self):
        """Update search_text field with all searchable content in lowercase"""
        search_parts = []
        
        # Add titles and descriptions from all languages
        for lang_data in self.translations.values():
            if isinstance(lang_data, dict):
                title = lang_data.get('title', '')
                description = lang_data.get('description', '')
                if title:
                    search_parts.append(title.lower())
                if description:
                    search_parts.append(description.lower())
        
        # Add other searchable fields in lowercase
        if self.city:
            search_parts.append(self.city.lower())
        if self.user.first_name:
            search_parts.append(self.user.first_name.lower())
        if self.user.last_name:
            search_parts.append(self.user.last_name.lower())
        if self.user.username:
            search_parts.append(self.user.username.lower())
        if self.phone:
            search_parts.append(self.phone.lower())
        if self.email:
            search_parts.append(self.email.lower())
        if self.instagram:
            search_parts.append(self.instagram.lower())
        if self.facebook:
            search_parts.append(self.facebook.lower())
        if self.whatsapp:
            search_parts.append(self.whatsapp.lower())
        if self.telegram:
            search_parts.append(self.telegram.lower())
        if self.website:
            search_parts.append(self.website.lower())
        
        self.search_text = ' '.join(search_parts)
        self.save(update_fields=['search_text'])
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update search text after save
        if not kwargs.get('update_fields') or 'search_text' not in kwargs.get('update_fields'):
            self.update_search_text()
        
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
            models.Index(fields=['search_text']),  # Index for search performance
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
