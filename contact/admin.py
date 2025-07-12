from django.contrib import admin
from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'email', 'subject', 'created_at', 
        'is_read', 'is_replied'
    ]
    list_filter = ['is_read', 'is_replied', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['created_at', 'ip_address', 'user_agent']
    list_per_page = 25
    
    fieldsets = (
        ('Thông tin liên hệ', {
            'fields': ('name', 'email', 'subject', 'message')
        }),
        ('Trạng thái', {
            'fields': ('is_read', 'is_replied', 'admin_notes')
        }),
        ('Thông tin kỹ thuật', {
            'fields': ('created_at', 'ip_address', 'user_agent'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_read', 'mark_as_replied', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(
            request, 
            f'{updated} tin nhắn đã được đánh dấu là đã đọc.'
        )
    mark_as_read.short_description = "Đánh dấu đã đọc"
    
    def mark_as_replied(self, request, queryset):
        updated = queryset.update(is_replied=True)
        self.message_user(
            request, 
            f'{updated} tin nhắn đã được đánh dấu là đã phản hồi.'
        )
    mark_as_replied.short_description = "Đánh dấu đã phản hồi"
    
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(
            request, 
            f'{updated} tin nhắn đã được đánh dấu là chưa đọc.'
        )
    mark_as_unread.short_description = "Đánh dấu chưa đọc" 