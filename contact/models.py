from django.db import models
from django.utils import timezone


class ContactMessage(models.Model):
    """Model to store contact form submissions"""
    
    name = models.CharField(max_length=100, verbose_name='Tên')
    email = models.EmailField(verbose_name='Email')
    subject = models.CharField(max_length=200, verbose_name='Tiêu đề')
    message = models.TextField(verbose_name='Nội dung')
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Thời gian gửi')
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name='IP Address')
    user_agent = models.TextField(blank=True, verbose_name='User Agent')
    
    # Status
    is_read = models.BooleanField(default=False, verbose_name='Đã đọc')
    is_replied = models.BooleanField(default=False, verbose_name='Đã phản hồi')
    admin_notes = models.TextField(blank=True, verbose_name='Ghi chú của admin')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Tin nhắn liên hệ'
        verbose_name_plural = 'Tin nhắn liên hệ'
    
    def __str__(self):
        return f"{self.name} - {self.subject} ({self.created_at.strftime('%d/%m/%Y')})"
    
    def mark_as_read(self):
        """Mark message as read"""
        self.is_read = True
        self.save(update_fields=['is_read'])
    
    def mark_as_replied(self):
        """Mark message as replied"""
        self.is_replied = True
        self.save(update_fields=['is_replied']) 