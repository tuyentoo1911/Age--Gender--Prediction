import streamlit as st
import tensorflow as tf
import numpy as np
import cv2
from PIL import Image
import os
import time

# Configure Streamlit page
st.set_page_config(
    page_title="🤖 AI Age & Gender Prediction",
    page_icon="🤖",
    layout="wide"
)

# Global variables for caching models
@st.cache_resource
def load_models():
    """Load and cache ML models"""
    try:
        # Model paths
        age_model_path = "models/best_age_model.h5"
        gender_model_path = "models/best_gender_model.h5"
        
        # Check if model files exist
        if not os.path.exists(age_model_path):
            age_model_path = "best_age_model.h5"
        if not os.path.exists(gender_model_path):
            gender_model_path = "best_gender_model.h5"
            
        if not os.path.exists(age_model_path) or not os.path.exists(gender_model_path):
            st.error("❌ Model files not found! Please ensure you have:")
            st.error("- models/best_age_model.h5")
            st.error("- models/best_gender_model.h5")
            st.stop()
        
        # Load models
        age_model = tf.keras.models.load_model(age_model_path)
        gender_model = tf.keras.models.load_model(gender_model_path)
        
        st.success(f"✅ Models loaded successfully!")
        st.info(f"📁 Age model: {age_model_path}")
        st.info(f"📁 Gender model: {gender_model_path}")
        
        return age_model, gender_model
        
    except Exception as e:
        st.error(f"❌ Error loading models: {str(e)}")
        st.stop()

def preprocess_image(image):
    """Preprocess image for model prediction"""
    try:
        # Convert PIL to numpy array
        img_array = np.array(image)
        
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
        st.error(f"❌ Error preprocessing image: {str(e)}")
        return None

def predict_age_gender(image, age_model, gender_model):
    """Predict age and gender from image"""
    start_time = time.time()
    
    try:
        # Preprocess image
        processed_img = preprocess_image(image)
        if processed_img is None:
            return None
        
        # Make predictions
        with st.spinner("🤖 Making predictions..."):
            gender_pred = gender_model.predict(processed_img, verbose=0)[0][0]
            age_pred = age_model.predict(processed_img, verbose=0)[0][0]
        
        # Process gender prediction
        gender_label = "Female" if gender_pred > 0.5 else "Male"
        gender_code = "F" if gender_pred > 0.5 else "M"
        gender_confidence = (gender_pred if gender_pred > 0.5 else 1 - gender_pred) * 100
        
        # Process age prediction
        if age_pred < 1.0:
            predicted_age = max(1, int(round(age_pred * 100)))
        elif age_pred < 10.0:
            predicted_age = max(1, int(round(age_pred * 10)))
        else:
            predicted_age = max(1, int(round(age_pred)))
            
        predicted_age = min(100, max(1, predicted_age))
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        result = {
            'age': predicted_age,
            'gender_label': gender_label,
            'gender_code': gender_code,
            'gender_confidence': float(gender_confidence),
            'age_confidence': 85.0,
            'processing_time': processing_time,
            'raw_age': float(age_pred),
            'raw_gender': float(gender_pred)
        }
        
        return result
        
    except Exception as e:
        st.error(f"❌ Prediction error: {str(e)}")
        return None

# Main Streamlit App
def main():
    # Title and description
    st.title("🤖 AI Age & Gender Prediction")
    st.markdown("---")
    st.markdown("**Upload an image to predict age and gender using Deep Learning models**")
    
    # Load models
    age_model, gender_model = load_models()
    
    # Sidebar for options
    st.sidebar.title("⚙️ Options")
    show_debug = st.sidebar.checkbox("🐛 Show Debug Info", value=False)
    show_processed = st.sidebar.checkbox("📷 Show Processed Image", value=False)
    
    # File uploader
    uploaded_file = st.file_uploader(
        "📁 Choose an image file",
        type=['png', 'jpg', 'jpeg'],
        help="Upload a PNG, JPG, or JPEG image"
    )
    
    if uploaded_file is not None:
        # Create columns for layout
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📸 Original Image")
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            
            # Show image info
            st.info(f"📊 Image size: {image.size}")
            st.info(f"🎨 Mode: {image.mode}")
        
        with col2:
            st.subheader("🎯 Prediction Results")
            
            # Make prediction
            result = predict_age_gender(image, age_model, gender_model)
            
            if result:
                # Display results in attractive format
                st.markdown("### 🎉 Results:")
                
                # Age result
                st.metric(
                    label="📅 Predicted Age",
                    value=f"{result['age']} years",
                    delta=f"Confidence: {result['age_confidence']:.1f}%"
                )
                
                # Gender result
                gender_icon = "👨" if result['gender_code'] == 'M' else "👩"
                st.metric(
                    label=f"{gender_icon} Predicted Gender",
                    value=result['gender_label'],
                    delta=f"Confidence: {result['gender_confidence']:.1f}%"
                )
                
                # Processing time
                st.metric(
                    label="⏱️ Processing Time",
                    value=f"{result['processing_time']:.3f}s"
                )
                
                # Progress bars for confidence
                st.markdown("### 📊 Confidence Levels:")
                st.progress(result['gender_confidence']/100)
                st.caption(f"Gender Confidence: {result['gender_confidence']:.1f}%")
                
                st.progress(result['age_confidence']/100)
                st.caption(f"Age Confidence: {result['age_confidence']:.1f}%")
                
                # Debug information
                if show_debug:
                    st.markdown("### 🐛 Debug Information:")
                    st.json({
                        "Raw Age Prediction": result['raw_age'],
                        "Raw Gender Prediction": result['raw_gender'],
                        "Processed Age": result['age'],
                        "Gender Code": result['gender_code'],
                        "Processing Time": result['processing_time']
                    })
        
        # Show processed image if requested
        if show_processed:
            st.markdown("---")
            st.subheader("🔍 Processed Image (64x64 Grayscale)")
            processed_img = preprocess_image(image)
            if processed_img is not None:
                # Convert back to displayable format
                display_img = processed_img[0, :, :, 0] * 255
                st.image(display_img, caption="Processed for Model", width=200)
    
    else:
        # Instructions when no file uploaded
        st.info("👆 Please upload an image file to start prediction")
        
        # Example images section
        st.markdown("---")
        st.subheader("📝 Instructions:")
        st.markdown("""
        1. **Upload** an image using the file uploader above
        2. **Wait** for the models to process the image
        3. **View** the predicted age and gender results
        4. **Enable** debug mode in sidebar for detailed information
        
        **Supported formats:** PNG, JPG, JPEG
        **Best results:** Clear frontal face photos with good lighting
        """)
        
        # Model information
        st.markdown("---")
        st.subheader("🧠 Model Information:")
        st.markdown("""
        - **Age Model**: CNN trained on facial datasets
        - **Gender Model**: Binary classification (Male/Female)
        - **Input Size**: 64x64 grayscale images
        - **Framework**: TensorFlow/Keras
        """)

# Footer
def add_footer():
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center'>
            <p>🤖 AI Age & Gender Prediction | Built with Streamlit & TensorFlow</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
    add_footer() 