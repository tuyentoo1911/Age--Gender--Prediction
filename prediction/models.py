from django.db import models
from django.utils import timezone
import os


def upload_image_path(instance, filename):
    """Generate upload path for images"""
    ext = filename.split('.')[-1]
    filename = f"prediction_{timezone.now().strftime('%Y%m%d_%H%M%S')}.{ext}"
    return os.path.join('uploads', filename)


class PredictionResult(models.Model):
    """Model to store prediction results"""
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    
    # Image and upload info
    image = models.ImageField(upload_to=upload_image_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    # Prediction results
    predicted_age = models.IntegerField(null=True, blank=True)
    predicted_gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    
    # Confidence scores
    age_confidence = models.FloatField(null=True, blank=True)
    gender_confidence = models.FloatField(null=True, blank=True)
    
    # Processing info
    processing_time = models.FloatField(null=True, blank=True)  # in seconds
    is_successful = models.BooleanField(default=False)
    error_message = models.TextField(blank=True)
    
    # Optional user info (for analytics)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        if self.is_successful:
            return f"Prediction: {self.predicted_age} years, {self.get_predicted_gender_display()}"
        return f"Failed prediction at {self.uploaded_at}"
    
    def get_image_url(self):
        """Get image URL safely"""
        if self.image:
            return self.image.url
        return None
    
    def delete(self, *args, **kwargs):
        """Delete image file when model instance is deleted"""
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs) 