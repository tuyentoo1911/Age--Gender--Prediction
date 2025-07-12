# 🤖 AI Age & Gender Prediction - Streamlit App

Ứng dụng Streamlit đơn giản để test model AI dự đoán tuổi và giới tính.

## 🚀 Cách sử dụng

### 1. Cài đặt dependencies

```bash
pip install -r requirements_streamlit.txt
```

### 2. Chạy ứng dụng

#### Windows:

```bash
run_streamlit.bat
```

#### Linux/Mac:

```bash
chmod +x run_streamlit.sh
./run_streamlit.sh
```

#### Hoặc chạy trực tiếp:

```bash
streamlit run app.py
```

### 3. Truy cập ứng dụng

Mở trình duyệt và truy cập: `http://localhost:8501`

## 📁 Cần có các file model

Đảm bảo bạn có một trong những cách sau:

**Cách 1:** Đặt trong thư mục `models/`

```
models/
├── best_age_model.h5
└── best_gender_model.h5
```

**Cách 2:** Đặt trong thư mục gốc

```
├── app.py
├── best_age_model.h5
└── best_gender_model.h5
```

## ✨ Tính năng

- 📸 **Upload ảnh** từ máy tính
- 🎯 **Dự đoán tuổi** và **giới tính**
- 📊 **Hiển thị confidence scores** với progress bars
- 🐛 **Debug mode** để xem raw predictions
- 🔍 **Processed image preview** (64x64 grayscale)
- ⏱️ **Processing time** measurement
- 📱 **Responsive layout** với 2 columns

## 🎨 Giao diện

- **Sidebar** với options
- **Main area** hiển thị ảnh gốc và kết quả
- **Metrics** với icons đẹp mắt
- **Progress bars** cho confidence levels
- **JSON debug** information (tùy chọn)

## 🔧 Troubleshooting

### Lỗi model không tìm thấy:

```
❌ Model files not found! Please ensure you have:
- models/best_age_model.h5
- models/best_gender_model.h5
```

**Giải quyết:** Copy file model vào đúng thư mục

### Lỗi import:

```
ModuleNotFoundError: No module named 'streamlit'
```

**Giải quyết:**

```bash
pip install streamlit
```

### Lỗi TensorFlow:

```
ImportError: No module named 'tensorflow'
```

**Giải quyết:**

```bash
pip install tensorflow
```

## 📊 Demo Flow

1. **Load app** → Models được cache automatically
2. **Upload image** → Preprocessing (resize, grayscale, normalize)
3. **Predict** → Run through both age & gender models
4. **Display results** → Pretty metrics với confidence scores
5. **Debug info** → Raw predictions và processing details

## 🎯 Best Results

- **Clear frontal face photos**
- **Good lighting**
- **Single person** in image
- **Formats:** PNG, JPG, JPEG
- **Size:** Any size (app sẽ resize automatically)

## 🚀 Performance

- **First load:** ~2-3 seconds (model loading)
- **Subsequent predictions:** ~0.1-0.3 seconds
- **Memory usage:** ~500MB (TensorFlow + models)
- **Model caching:** Streamlit `@st.cache_resource`

---

🎉 **Happy testing!** Upload một ảnh và xem AI predict như thế nào!
