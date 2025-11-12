from django.db import models
from django.contrib.auth import get_user_model
from services.models import Service

User = get_user_model()


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='reviews')
    
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update service rating
        self.service.update_rating()
        # Update user rating
        self.service.user.update_rating()
    
    def __str__(self):
        return f"Review by {self.user.username} for {self.service} - {self.rating}★"
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'service']
