from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Service, Favorite


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['get_name', 'slug', 'icon_preview', 'parent', 'order', 'created_at']
    list_filter = ['parent']
    search_fields = ['slug', 'translations']
    prepopulated_fields = {'slug': ('slug',)}
    ordering = ['order', 'slug']
    readonly_fields = ['icon_preview']
    
    def get_name(self, obj):
        return obj.get_translation('ru')
    get_name.short_description = 'Name'
    
    def icon_preview(self, obj):
        if obj.icon:
            # Check if it's a GIF file for special handling
            is_gif = str(obj.icon.name).lower().endswith('.gif')
            if is_gif:
                return format_html(
                    '<div style="position: relative;">'
                    '<img src="{}" width="40" height="40" style="object-fit: cover; border-radius: 4px; border: 2px solid #4CAF50;" />'
                    '<span style="position: absolute; top: -5px; right: -5px; background: #4CAF50; color: white; border-radius: 50%; width: 16px; height: 16px; font-size: 10px; display: flex; align-items: center; justify-content: center;">GIF</span>'
                    '</div>',
                    obj.icon.url
                )
            else:
                return format_html('<img src="{}" width="40" height="40" style="object-fit: cover; border-radius: 4px;" />', obj.icon.url)
        return 'No icon'
    icon_preview.short_description = 'Icon'


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['get_title', 'user', 'category', 'status', 'price', 'city', 'rating', 'is_active', 'created_at']
    list_filter = ['status', 'category', 'city', 'is_active', 'created_at']
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
