from django.contrib import admin
from .models import PredictionResult


@admin.register(PredictionResult)
class PredictionResultAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'uploaded_at', 'predicted_age', 'predicted_gender', 
        'is_successful', 'processing_time', 'ip_address'
    ]
    list_filter = [
        'is_successful', 'predicted_gender', 'uploaded_at'
    ]
    search_fields = ['ip_address', 'user_agent']
    readonly_fields = [
        'uploaded_at', 'processing_time', 'ip_address', 'user_agent'
    ]
    list_per_page = 25
    
    fieldsets = (
        ('Thông tin ảnh', {
            'fields': ('image', 'uploaded_at')
        }),
        ('Kết quả dự đoán', {
            'fields': (
                'predicted_age', 'predicted_gender', 
                'age_confidence', 'gender_confidence',
                'is_successful', 'error_message'
            )
        }),
        ('Thông tin kỹ thuật', {
            'fields': ('processing_time', 'ip_address', 'user_agent'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related()
    
    def has_add_permission(self, request):
        return False  # Prevent manual creation
    
    actions = ['delete_selected'] 