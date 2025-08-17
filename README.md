# 🤖 Nhận diện Tuổi & Giới tính - Django Web Application

Ứng dụng web sử dụng AI để nhận diện tuổi và giới tính từ hình ảnh khuôn mặt, được xây dựng với Django và TensorFlow.

## ✨ Tính năng

- 📸 **Upload ảnh từ máy tính** - Hỗ trợ JPG, PNG, WEBP
- 📷 **Chụp ảnh trực tiếp từ camera** - Sử dụng camera của thiết bị
- 🧠 **AI dự đoán thông minh** - Độ chính xác cao >85%
- 📱 **Responsive design** - Hoạt động mượt mà trên mọi thiết bị
- 📊 **Thống kê và lịch sử** - Theo dõi các dự đoán đã thực hiện
- 💬 **Form liên hệ** - Gửi phản hồi và câu hỏi
- 🔒 **Bảo mật dữ liệu** - Không lưu trữ ảnh cá nhân lâu dài

## 🛠️ Công nghệ sử dụng

- **Backend**: Django 4.2+ (Python)
- **Frontend**: Bootstrap 5 + HTML/CSS/JavaScript
- **Machine Learning**: TensorFlow/Keras
- **Database**: SQLite (dev) / PostgreSQL (production)
- **Deployment**: Docker + Nginx + Gunicorn
- **UI Framework**: Crispy Forms với Bootstrap 5

## 📋 Yêu cầu hệ thống

- Python 3.11+
- pip
- Virtual environment (khuyến nghị)
- Docker & Docker Compose (cho deployment)

## 🚀 Cài đặt và Chạy

### 1. Clone repository

```bash
git clone <repository-url>
cd face-prediction-django
```

### 2. Tạo và kích hoạt virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

### 3. Cài đặt dependencies

```bash
pip install -r django_requirements.txt
```

### 4. Thiết lập database

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5. Collect static files

```bash
python manage.py collectstatic
```

### 6. Chạy development server

```bash
python manage.py runserver
```

Truy cập: http://localhost:8000

## 🐳 Deployment với Docker

### 1. Build và chạy với Docker Compose

```bash
docker-compose up --build
```

### 2. Truy cập ứng dụng

- **Website**: http://localhost
- **Admin**: http://localhost/admin (admin/admin123)

### 3. Dừng services

```bash
docker-compose down
```

## 📁 Cấu trúc Project

```
face-prediction-django/
├── face_prediction_project/     # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── prediction/                  # Main prediction app
│   ├── models.py               # Database models
│   ├── views.py                # Views logic
│   ├── forms.py                # Forms definition
│   ├── utils.py                # ML utilities
│   ├── urls.py                 # URL patterns
│   └── admin.py                # Admin interface
├── contact/                     # Contact form app
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── urls.py
├── templates/                   # HTML templates
│   ├── base.html               # Base template
│   ├── prediction/             # Prediction templates
│   └── contact/                # Contact templates
├── static/                      # Static files (CSS, JS, images)
├── media/                       # Uploaded files
├── models/                      # ML model files
│   ├── best_gender_model.h5
│   └── best_age_model.h5
├── requirements.txt
├── manage.py
├── Dockerfile
├── docker-compose.yml
└── nginx.conf
```

## 🧠 Mô hình Machine Learning

### Gender Model

- **Kiến trúc**: CNN Binary Classification
- **Input**: 64x64 grayscale images
- **Output**: Male/Female với confidence score
- **Accuracy**: ~87%

### Age Model

- **Kiến trúc**: CNN Regression
- **Input**: 64x64 grayscale images
- **Output**: Age prediction (0-110 years)
- **MAE**: ~3-5 years

## 🔧 Cấu hình

### Environment Variables

Tạo file `.env` để cấu hình:

```env
DEBUG=False
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@host:port/dbname
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com
```

### Database Settings

**Development (SQLite)**:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**Production (PostgreSQL)**:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'face_prediction',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 📚 API Documentation

### Prediction Endpoints

- `GET /` - Trang chủ với form upload
- `POST /predict/` - Dự đoán từ file upload
- `POST /camera-predict/` - Dự đoán từ camera (AJAX)
- `GET /history/` - Lịch sử dự đoán
- `GET /stats/` - Thống kê hệ thống

### Contact Endpoints

- `GET /contact/` - Form liên hệ
- `POST /contact/` - Gửi tin nhắn liên hệ

## 🛡️ Bảo mật

- CSRF protection enabled
- XSS protection headers
- File upload validation
- SQL injection protection (Django ORM)
- Secure static file serving
- Rate limiting (có thể thêm django-ratelimit)

## 🔍 Monitoring & Logging

- Django logging configuration
- Nginx access logs
- Health check endpoint: `/health/`
- Admin interface để quản lý data

## 🚀 Deployment Options

### 1. Heroku

```bash
# Install Heroku CLI và login
heroku login
heroku create your-app-name
git push heroku main
```

### 2. VPS với Docker

```bash
# Trên server
docker-compose -f docker-compose.prod.yml up -d
```

### 3. AWS/GCP/Azure

- Sử dụng container services (ECS, Cloud Run, Container Instances)
- Cấu hình load balancer và SSL certificate
- Sử dụng managed database services

## 🔧 Troubleshooting

### Lỗi thường gặp

**1. Model files không tìm thấy**

```bash
# Đảm bảo model files ở đúng vị trí
cp best_*.h5 models/
```

**2. CSRF token missing**

```html
<!-- Thêm vào form -->
{% csrf_token %}
```

**3. Static files không load**

```bash
python manage.py collectstatic --clear
```

**4. Memory error khi load model**

- Tăng RAM cho container
- Sử dụng model quantization
- Load model lazy loading

## 📈 Performance Optimization

### Backend

- Cache models in memory
- Use database connection pooling
- Optimize image processing
- Add Redis for session/cache

### Frontend

- Compress images before upload
- Use image lazy loading
- Minimize CSS/JS files
- Add PWA capabilities

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

- **Tô Trần Tuyển** - [GitHub](https://github.com/tuyentoo1911)

## 🙏 Acknowledgments

- TensorFlow team for the ML framework
- Django community for the web framework
- Bootstrap team for the UI components
- OpenCV for image processing utilities

---

📧 **Contact**: support@yourdomain.com  
🌐 **Website**: https://yourdomain.com  
📱 **Demo**: https://demo.yourdomain.com
