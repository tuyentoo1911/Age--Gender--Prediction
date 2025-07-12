import tensorflow as tf
import numpy as np
import cv2
import os
from PIL import Image
from django.conf import settings
import logging
import base64
from io import BytesIO
import time

logger = logging.getLogger(__name__)

# Global variables to cache models
_gender_model = None
_age_model = None


def load_models():
    """Load and cache ML models"""
    global _gender_model, _age_model
    
    if _gender_model is None or _age_model is None:
        try:
            models_dir = getattr(settings, 'ML_MODELS_DIR', settings.BASE_DIR)
            
            gender_model_path = os.path.join(models_dir, 'best_gender_model.h5')
            age_model_path = os.path.join(models_dir, 'best_age_model.h5')
            
            # Check if model files exist
            if not os.path.exists(gender_model_path):
                # Try to find in current directory
                gender_model_path = os.path.join(settings.BASE_DIR, 'best_gender_model.h5')
            
            if not os.path.exists(age_model_path):
                # Try to find in current directory
                age_model_path = os.path.join(settings.BASE_DIR, 'best_age_model.h5')
            
            if not os.path.exists(gender_model_path) or not os.path.exists(age_model_path):
                raise FileNotFoundError("Model files not found")
            
            _gender_model = tf.keras.models.load_model(gender_model_path)
            _age_model = tf.keras.models.load_model(age_model_path)
            
            print(f"✅ Models loaded successfully:")
            print(f"   Gender model: {gender_model_path}")
            print(f"   Age model: {age_model_path}")
            print(f"   Gender model output shape: {_gender_model.output_shape}")
            print(f"   Age model output shape: {_age_model.output_shape}")
            
            logger.info("Models loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            raise e
    
    return _gender_model, _age_model


def preprocess_image(image_input):
    """
    Preprocess image for model prediction
    
    Args:
        image_input: PIL Image, numpy array, or file path
    
    Returns:
        Preprocessed image array ready for model prediction
    """
    try:
        # Convert input to numpy array
        if isinstance(image_input, str):
            # File path
            img = cv2.imread(image_input)
            if img is None:
                raise ValueError("Could not load image from path")
            img_array = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        elif hasattr(image_input, 'read'):
            # File object
            img = Image.open(image_input)
            img_array = np.array(img)
        elif isinstance(image_input, Image.Image):
            # PIL Image
            img_array = np.array(image_input)
        elif isinstance(image_input, np.ndarray):
            # Numpy array
            img_array = image_input
        else:
            raise ValueError("Unsupported image input type")
        
        # Convert to grayscale if needed
        if len(img_array.shape) == 3:
            img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        
        # Resize to 64x64 (model expected size)
        img_resized = cv2.resize(img_array, (64, 64))
        
        # Normalize to [0,1]
        img_normalized = img_resized.astype('float32') / 255.0
        
        # Add batch dimension and channel dimension
        img_processed = np.expand_dims(img_normalized, axis=[0, -1])
        
        return img_processed
        
    except Exception as e:
        logger.error(f"Error preprocessing image: {e}")
        raise e


def predict_age_gender(image_input):
    """
    Predict age and gender from image
    
    Args:
        image_input: PIL Image, numpy array, or file path
    
    Returns:
        dict: Prediction results with age, gender, and confidence scores
    """
    start_time = time.time()
    
    try:
        # Load models
        gender_model, age_model = load_models()
        
        # Preprocess image
        processed_img = preprocess_image(image_input)
        
        # Make predictions
        gender_pred = gender_model.predict(processed_img, verbose=0)[0][0]
        age_pred = age_model.predict(processed_img, verbose=0)[0][0]
        
        # Debug: Log raw predictions
        print(f"RAW PREDICTIONS - Gender: {gender_pred}, Age: {age_pred}")
        
        # Process gender prediction
        gender_label = "Female" if gender_pred > 0.5 else "Male"
        gender_code = "F" if gender_pred > 0.5 else "M"
        gender_confidence = (gender_pred if gender_pred > 0.5 else 1 - gender_pred) * 100
        
        # Process age prediction - handle different model output ranges
        if age_pred < 1.0:
            # Model outputs normalized value (0-1), scale to age range
            predicted_age = max(1, int(round(age_pred * 100)))
        elif age_pred < 10.0:
            # Model outputs value in range 0-10, scale to age range  
            predicted_age = max(1, int(round(age_pred * 10)))
        else:
            # Model outputs actual age
            predicted_age = max(1, int(round(age_pred)))
            
        # Ensure reasonable age range
        predicted_age = min(100, max(1, predicted_age))
        
        print(f"PROCESSED AGE: Raw={age_pred} -> Final={predicted_age}")
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        result = {
            'age': predicted_age,
            'gender_label': gender_label,
            'gender_code': gender_code,
            'gender_confidence': float(gender_confidence),
            'age_confidence': 85.0,  # Age models don't typically return confidence (as percentage)
            'processing_time': processing_time,
            'success': True,
            'error': None
        }
        
        logger.info(f"Prediction successful: {result}")
        return result
        
    except Exception as e:
        error_msg = f"Prediction error: {str(e)}"
        logger.error(error_msg)
        
        return {
            'age': None,
            'gender_label': None,
            'gender_code': None,
            'gender_confidence': None,
            'age_confidence': None,
            'processing_time': time.time() - start_time,
            'success': False,
            'error': error_msg
        }


def base64_to_image(base64_string):
    """
    Convert base64 string to PIL Image
    
    Args:
        base64_string: Base64 encoded image string
    
    Returns:
        PIL Image object
    """
    try:
        # Remove data URL prefix if present
        if 'base64,' in base64_string:
            base64_string = base64_string.split('base64,')[1]
        
        # Decode base64
        image_data = base64.b64decode(base64_string)
        
        # Create PIL Image
        image = Image.open(BytesIO(image_data))
        
        return image
        
    except Exception as e:
        logger.error(f"Error converting base64 to image: {e}")
        raise e


def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip 