from django import forms
from django.core.exceptions import ValidationError
from PIL import Image
import os


class ImageUploadForm(forms.Form):
    """Form for uploading images for prediction"""
    image = forms.ImageField(
        label='Chọn ảnh khuôn mặt',
        help_text='Định dạng: JPG, PNG. Kích thước tối đa: 10MB',
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*',
            'id': 'imageInput'
        })
    )
    
    def clean_image(self):
        image = self.cleaned_data.get('image')
        
        if image:
            # Check file size (10MB limit)
            if image.size > 10 * 1024 * 1024:
                raise ValidationError('Kích thước ảnh không được vượt quá 10MB.')
            
            # Check file extension
            valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
            ext = os.path.splitext(image.name)[1].lower()
            if ext not in valid_extensions:
                raise ValidationError('Chỉ chấp nhận file ảnh định dạng JPG, PNG, WEBP.')
            
            # Check if it's a valid image
            try:
                img = Image.open(image)
                img.verify()
                
                # Reset file pointer after verify
                image.seek(0)
                
                # Check image dimensions (minimum size)
                img = Image.open(image)
                width, height = img.size
                if width < 64 or height < 64:
                    raise ValidationError('Ảnh quá nhỏ. Kích thước tối thiểu là 64x64 pixels.')
                
                # Reset file pointer again
                image.seek(0)
                
            except Exception as e:
                raise ValidationError(f'File không phải là ảnh hợp lệ: {str(e)}')
        
        return image


class CameraForm(forms.Form):
    """Form for camera capture (hidden input to receive base64 data)"""
    camera_data = forms.CharField(
        widget=forms.HiddenInput(),
        required=False
    ) 