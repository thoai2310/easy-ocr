# OCR API với EasyOCR

Dự án OCR sử dụng EasyOCR để scan image và PDF thành text. Model chạy local với GPU support, nhanh và hiệu quả.

## Yêu cầu hệ thống

- NVIDIA GPU (RTX 3050 6GB hoặc tương đương) - **Khuyến nghị**
- Docker và Docker Compose
- NVIDIA Docker runtime (nvidia-docker2)
- **Lưu ý**: Có thể chạy trên CPU nhưng sẽ chậm hơn nhiều

## Cài đặt

### 1. Cài đặt Docker Desktop và NVIDIA Container Toolkit

#### Windows:
1. Cài đặt **Docker Desktop for Windows** từ: https://www.docker.com/products/docker-desktop
2. Cài đặt **NVIDIA Container Toolkit**:
   - Download từ: https://github.com/NVIDIA/nvidia-docker/releases
   - Hoặc sử dụng WSL2 với Docker Desktop và cài đặt trong WSL2

#### Linux (Ubuntu/Debian):
```bash
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update
sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker
```

### 2. Build và chạy Docker container

```bash
# Build image
docker-compose build

# Chạy container
docker-compose up -d

# Xem logs
docker-compose logs -f
```

Lần đầu chạy sẽ mất thời gian để download model EasyOCR (~500MB cho tiếng Việt và tiếng Anh).

## Sử dụng API

### Health Check

```bash
GET http://localhost:8000/health
```

### OCR Endpoint

**URL:** `POST http://localhost:8000/ocr`

**Body:** Form-data với key `file` và value là file cần OCR

## Test với Postman

1. Mở Postman
2. Tạo request mới:
   - Method: `POST`
   - URL: `http://localhost:8000/ocr`
3. Chọn tab **Body**
4. Chọn **form-data**
5. Thêm key `file` (type: File)
6. Chọn file image hoặc PDF
7. Click **Send**

### Response mẫu:

```json
{
    "success": true,
    "filename": "example.pdf",
    "pages": [
        {
            "page": 1,
            "method": "easyocr",
            "text": "Nội dung text đã được OCR...",
            "time": 2.45
        }
    ],
    "total_pages": 1,
    "processing_time": 2.5
}
```

## Test với cURL

```bash
# Test với image
curl -X POST "http://localhost:8000/ocr" \
  -F "file=@/path/to/image.jpg"

# Test với PDF
curl -X POST "http://localhost:8000/ocr" \
  -F "file=@/path/to/document.pdf"
```

## Cấu trúc project

```
.
├── app.py              # FastAPI server
├── ocr_service.py      # OCR service với EasyOCR
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker image definition
├── docker-compose.yml  # Docker compose config
├── README.md          # Documentation
└── QUICKSTART.md      # Quick start guide
```

## Tính năng

- ✅ OCR cho image (JPG, PNG, BMP, GIF, WebP)
- ✅ OCR cho PDF (nhiều trang, tự động phát hiện text-based PDF)
- ✅ Hỗ trợ tiếng Việt và tiếng Anh
- ✅ Tự động sử dụng GPU nếu có
- ✅ Nhanh và hiệu quả (2-5 giây/ảnh với GPU)
- ✅ API REST với FastAPI
- ✅ Docker containerization

## Lưu ý

- Model EasyOCR sẽ được cache trong thư mục `~/.EasyOCR/` sau lần download đầu tiên (~500MB)
- RTX 3050 6GB đủ để chạy EasyOCR với GPU, tốc độ nhanh (2-5 giây/ảnh)
- PDF nhiều trang sẽ được xử lý từng trang một
- PDF text-based sẽ được extract trực tiếp (không cần OCR) để tăng tốc
- Thời gian xử lý phụ thuộc vào kích thước và độ phức tạp của file
- Nếu không có GPU, EasyOCR sẽ tự động fallback về CPU (chậm hơn 5-10 lần)

## Troubleshooting

### Lỗi CUDA/GPU không được nhận diện

**Windows:**
- Đảm bảo Docker Desktop đã bật WSL2 backend
- Kiểm tra trong Docker Desktop Settings > Resources > WSL Integration
- Chạy trong WSL2 terminal:
```bash
docker run --rm --gpus all nvidia/cuda:12.1.1-base-ubuntu22.04 nvidia-smi
```

**Linux:**
```bash
docker run --rm --gpus all nvidia/cuda:12.1.1-base-ubuntu22.04 nvidia-smi
```

### EasyOCR chạy chậm

- Kiểm tra xem GPU có được sử dụng không: xem logs khi khởi động
- Nếu không có GPU, EasyOCR sẽ tự động dùng CPU (chậm hơn)
- Đảm bảo PyTorch với CUDA đã được cài đặt đúng

### Model download chậm

Model sẽ được cache sau lần download đầu tiên. Có thể pre-download model trước bằng cách chạy container và để nó download.

### Lỗi NumPy version

Nếu gặp lỗi về NumPy, đảm bảo `numpy<2.0.0` trong requirements.txt (đã được cấu hình sẵn).

## Performance

- **Với GPU (RTX 3050 6GB)**: ~2-5 giây/ảnh
- **Với CPU**: ~10-30 giây/ảnh
- **PDF text-based**: < 1 giây/trang (extract trực tiếp)
- **PDF scan**: ~2-5 giây/trang (với GPU)

## License

MIT
