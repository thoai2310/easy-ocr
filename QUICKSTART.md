# Quick Start Guide

## Bước 1: Kiểm tra Docker và GPU

```bash
# Kiểm tra Docker
docker --version

# Kiểm tra GPU (trong WSL2 hoặc Linux)
nvidia-smi
```

## Bước 2: Build và chạy

```bash
# Build Docker image
docker-compose build

# Chạy container
docker-compose up -d

# Xem logs (để theo dõi quá trình download model EasyOCR)
docker-compose logs -f
```

**Lưu ý**: Lần đầu chạy sẽ download model EasyOCR (~500MB), mất vài phút. Model sẽ được cache, lần sau nhanh hơn.

## Bước 3: Test API

### Với Postman:
1. Method: `POST`
2. URL: `http://localhost:8000/ocr`
3. Body > form-data:
   - Key: `file` (type: File)
   - Value: Chọn file image hoặc PDF
4. Click Send

### Với cURL:
```bash
curl -X POST "http://localhost:8000/ocr" -F "file=@test.jpg"
```

## Bước 4: Kiểm tra health

```bash
curl http://localhost:8000/health
```

## Kiểm tra GPU đang được sử dụng

Xem logs khi container khởi động:
```bash
docker-compose logs | grep -i "gpu\|cuda\|ready"
```

Nếu thấy "EASYOCR READY" (không có "CPU mode") nghĩa là đang dùng GPU.

## Troubleshooting

- **Model download chậm**: Lần đầu sẽ mất thời gian (~500MB), model sẽ được cache trong `~/.EasyOCR/`
- **Chạy chậm**: Kiểm tra xem GPU có được sử dụng không. Nếu không có GPU, sẽ tự động dùng CPU (chậm hơn 5-10 lần)
- **GPU không nhận diện**: Kiểm tra NVIDIA Docker runtime và CUDA version
- **Lỗi NumPy**: Đảm bảo `numpy<2.0.0` trong requirements.txt

## Performance Tips

- **Sử dụng GPU**: Tốc độ nhanh hơn 5-10 lần so với CPU
- **PDF text-based**: Sẽ được extract trực tiếp, không cần OCR (rất nhanh)
- **Resize ảnh lớn**: Nếu ảnh quá lớn, có thể resize trước để tăng tốc