from django.contrib import admin
from .models import Category, Service, Favorite


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['get_name', 'slug', 'parent', 'order', 'created_at']
    list_filter = ['parent']
    search_fields = ['slug']
    prepopulated_fields = {'slug': ('slug',)}
    ordering = ['order', 'slug']
    
    def get_name(self, obj):
        return obj.get_translation('ru')
    get_name.short_description = 'Name'


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['get_title', 'user', 'category', 'status', 'price', 'city', 'rating', 'is_active', 'created_at']
    list_filter = ['status', 'category', 'city', 'is_active', 'created_at', 'gender']
    search_fields = ['user__email', 'city', 'phone']
    readonly_fields = ['views_count', 'rating', 'reviews_count', 'created_at', 'updated_at']
    actions = ['approve_services', 'reject_services']
    
    def get_title(self, obj):
        trans = obj.get_translation('ru')
        return trans.get('title', 'No title')
    get_title.short_description = 'Title'
    
    def approve_services(self, request, queryset):
        queryset.update(status='approved')
        self.message_user(request, f'{queryset.count()} services approved.')
    approve_services.short_description = 'Approve selected services'
    
    def reject_services(self, request, queryset):
        queryset.update(status='rejected')
        self.message_user(request, f'{queryset.count()} services rejected.')
    reject_services.short_description = 'Reject selected services'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'service', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__email']
    readonly_fields = ['created_at']
