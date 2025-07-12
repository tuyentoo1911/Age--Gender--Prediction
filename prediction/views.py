from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.conf import settings
import json
import logging
from .forms import ImageUploadForm, CameraForm
from .models import PredictionResult
from .utils import predict_age_gender, base64_to_image, get_client_ip
from django.core.files.base import ContentFile
import base64
import io
from PIL import Image

logger = logging.getLogger(__name__)


class HomeView(View):
    """Home page view"""
    
    def get(self, request):
        upload_form = ImageUploadForm()
        camera_form = CameraForm()
        
        # Get recent predictions for display
        recent_predictions = PredictionResult.objects.filter(is_successful=True)[:6]
        
        context = {
            'upload_form': upload_form,
            'camera_form': camera_form,
            'recent_predictions': recent_predictions,
            'page_title': 'Nhận diện Tuổi & Giới tính'
        }
        return render(request, 'prediction/home.html', context)


class PredictView(View):
    """Handle image upload and prediction"""
    
    def post(self, request):
        upload_form = ImageUploadForm(request.POST, request.FILES)
        
        if upload_form.is_valid():
            try:
                # Get uploaded image
                image_file = upload_form.cleaned_data['image']
                
                # Create prediction result instance
                prediction = PredictionResult()
                prediction.image = image_file
                prediction.ip_address = get_client_ip(request)
                prediction.user_agent = request.META.get('HTTP_USER_AGENT', '')[:500]
                
                # Make prediction
                result = predict_age_gender(image_file)
                
                if result['success']:
                    # Save successful prediction
                    prediction.predicted_age = result['age']
                    prediction.predicted_gender = result['gender_code']
                    prediction.gender_confidence = result['gender_confidence']
                    prediction.age_confidence = result['age_confidence']
                    prediction.processing_time = result['processing_time']
                    prediction.is_successful = True
                    prediction.save()
                    
                    messages.success(request, 'Dự đoán thành công!')
                    
                    context = {
                        'prediction': prediction,
                        'result': result,
                        'page_title': 'Kết quả Dự đoán',
                        'debug': False  # Disable debug info display
                    }
                    
                    return render(request, 'prediction/result_fixed.html', context)
                
                else:
                    # Save failed prediction
                    prediction.is_successful = False
                    prediction.error_message = result['error']
                    prediction.processing_time = result['processing_time']
                    prediction.save()
                    
                    messages.error(request, f'Lỗi dự đoán: {result["error"]}')
                    
            except Exception as e:
                logger.error(f"Prediction error: {e}")
                messages.error(request, f'Có lỗi xảy ra: {str(e)}')
        
        else:
            # Form validation errors
            for field, errors in upload_form.errors.items():
                for error in errors:
                    messages.error(request, error)
        
        return redirect('home')


@method_decorator(csrf_exempt, name='dispatch')
class CameraPredictView(View):
    """Handle camera capture and prediction"""
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            base64_image = data.get('image_data')
            
            if not base64_image:
                return JsonResponse({'success': False, 'error': 'Không có dữ liệu ảnh'})
            
            # Convert base64 to PIL Image
            image = base64_to_image(base64_image)
            
            # Save image to file for storage
            img_io = io.BytesIO()
            image.save(img_io, format='JPEG', quality=85)
            img_content = ContentFile(img_io.getvalue(), name='camera_capture.jpg')
            
            # Create prediction result instance
            prediction = PredictionResult()
            prediction.image = img_content
            prediction.ip_address = get_client_ip(request)
            prediction.user_agent = request.META.get('HTTP_USER_AGENT', '')[:500]
            
            # Make prediction
            result = predict_age_gender(image)
            
            if result['success']:
                # Save successful prediction
                prediction.predicted_age = result['age']
                prediction.predicted_gender = result['gender_code']
                prediction.gender_confidence = result['gender_confidence']
                prediction.age_confidence = result['age_confidence']
                prediction.processing_time = result['processing_time']
                prediction.is_successful = True
                prediction.save()
                
                return JsonResponse({
                    'success': True,
                    'prediction_id': prediction.id,
                    'age': result['age'],
                    'gender': result['gender_label'],
                    'gender_confidence': f"{result['gender_confidence']:.1f}%",
                    'processing_time': f"{result['processing_time']:.2f}s",
                    'image_url': prediction.get_image_url()
                })
            
            else:
                # Save failed prediction
                prediction.is_successful = False
                prediction.error_message = result['error']
                prediction.processing_time = result['processing_time']
                prediction.save()
                
                return JsonResponse({
                    'success': False,
                    'error': result['error']
                })
                
        except Exception as e:
            logger.error(f"Camera prediction error: {e}")
            return JsonResponse({
                'success': False,
                'error': f'Lỗi xử lý: {str(e)}'
            })


class AboutView(View):
    """About page view"""
    
    def get(self, request):
        context = {
            'page_title': 'Giới thiệu'
        }
        return render(request, 'prediction/about.html', context)


class HistoryView(View):
    """View prediction history"""
    
    def get(self, request):
        predictions = PredictionResult.objects.filter(is_successful=True)[:50]
        
        context = {
            'predictions': predictions,
            'page_title': 'Lịch sử Dự đoán'
        }
        return render(request, 'prediction/history.html', context)


class StatsView(View):
    """View statistics"""
    
    def get(self, request):
        total_predictions = PredictionResult.objects.count()
        successful_predictions = PredictionResult.objects.filter(is_successful=True).count()
        
        # Gender distribution
        male_count = PredictionResult.objects.filter(
            is_successful=True, predicted_gender='M'
        ).count()
        female_count = PredictionResult.objects.filter(
            is_successful=True, predicted_gender='F'
        ).count()
        
        # Calculate gender percentages
        male_percentage = (male_count * 100 / successful_predictions) if successful_predictions > 0 else 0
        female_percentage = (female_count * 100 / successful_predictions) if successful_predictions > 0 else 0
        
        # Age distribution (simplified)
        age_counts = {
            '0-18': PredictionResult.objects.filter(
                is_successful=True, predicted_age__lt=18
            ).count(),
            '18-30': PredictionResult.objects.filter(
                is_successful=True, predicted_age__gte=18, predicted_age__lt=30
            ).count(),
            '30-50': PredictionResult.objects.filter(
                is_successful=True, predicted_age__gte=30, predicted_age__lt=50
            ).count(),
            '50+': PredictionResult.objects.filter(
                is_successful=True, predicted_age__gte=50
            ).count(),
        }
        
        # Calculate age range percentages
        age_ranges = {}
        for range_name, count in age_counts.items():
            percentage = (count * 100 / successful_predictions) if successful_predictions > 0 else 0
            age_ranges[range_name] = {
                'count': count,
                'percentage': percentage
            }
        
        context = {
            'total_predictions': total_predictions,
            'successful_predictions': successful_predictions,
            'success_rate': (successful_predictions / total_predictions * 100) if total_predictions > 0 else 0,
            'male_count': male_count,
            'female_count': female_count,
            'male_percentage': male_percentage,
            'female_percentage': female_percentage,
            'age_ranges': age_ranges,
            'page_title': 'Thống kê'
        }
        return render(request, 'prediction/stats.html', context) 