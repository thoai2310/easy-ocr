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

# Xem logs (để theo dõi quá trình download model)
docker-compose logs -f
```

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

## Troubleshooting

- **Model download chậm**: Lần đầu sẽ mất thời gian, model sẽ được cache
- **Out of Memory**: Giảm `max_new_tokens` trong `ocr_service.py` hoặc resize image
- **GPU không nhận diện**: Kiểm tra NVIDIA Docker runtime

