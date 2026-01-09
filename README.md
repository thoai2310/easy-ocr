# OCR API với Qwen2.5-VL 7B

Dự án OCR sử dụng Qwen2.5-VL 7B để scan image và PDF thành text. Model chạy local với GPU support.

## Yêu cầu hệ thống

- NVIDIA GPU (RTX 3050 6GB hoặc tương đương)
- Docker và Docker Compose
- NVIDIA Docker runtime (nvidia-docker2)

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

Lần đầu chạy sẽ mất thời gian để download model (~14GB).

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
    "text": "Nội dung text đã được OCR...",
    "processing_time": 2.45
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
├── ocr_service.py      # OCR service với Qwen2.5-VL
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker image definition
├── docker-compose.yml  # Docker compose config
└── README.md          # Documentation
```

## Lưu ý

- Model sẽ được cache trong thư mục `./models` sau lần download đầu tiên (~14GB)
- RTX 3050 6GB có thể xử lý được model với float16 quantization, nhưng có thể cần thời gian xử lý lâu hơn
- PDF nhiều trang sẽ được xử lý từng trang một
- Thời gian xử lý phụ thuộc vào kích thước và độ phức tạp của file
- Nếu gặp lỗi OOM (Out of Memory), có thể cần giảm `max_new_tokens` trong `ocr_service.py` hoặc resize image trước khi xử lý

## Troubleshooting

### Lỗi CUDA/GPU không được nhận diện

**Windows:**
- Đảm bảo Docker Desktop đã bật WSL2 backend
- Kiểm tra trong Docker Desktop Settings > Resources > WSL Integration
- Chạy trong WSL2 terminal:
```bash
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi
```

**Linux:**
```bash
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi
```

### Out of Memory

Nếu gặp lỗi OOM, có thể giảm batch size hoặc sử dụng CPU mode (chậm hơn).

### Model download chậm

Model sẽ được cache sau lần download đầu tiên. Có thể pre-download model trước.

## License

MIT

