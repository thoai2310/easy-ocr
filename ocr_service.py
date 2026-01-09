import time
import io
import logging
from typing import Dict, Any, List
from PIL import Image
from pdf2image import convert_from_bytes
from pypdf import PdfReader
import easyocr

logger = logging.getLogger(__name__)


class OCRService:
    def __init__(self):
        logger.info("Initializing OCR Service with EasyOCR")
        self._load_model()

    def _load_model(self):
        logger.info(">>> START loading EasyOCR")
        
        # Khởi tạo EasyOCR với tiếng Việt và tiếng Anh
        # EasyOCR tự động phát hiện GPU nếu có
        try:
            # ['vi', 'en'] - hỗ trợ tiếng Việt và tiếng Anh
            # gpu=True sẽ tự động sử dụng GPU nếu có
            self.reader = easyocr.Reader(
                ['vi', 'en'],
                gpu=True  # Tự động phát hiện GPU
            )
            logger.info(">>> EASYOCR READY")
        except Exception as e:
            logger.error(f"Failed to load EasyOCR: {e}")
            # Fallback: thử với CPU
            logger.warning("Trying with CPU...")
            try:
                self.reader = easyocr.Reader(
                    ['vi', 'en'],
                    gpu=False
                )
                logger.info(">>> EASYOCR READY (CPU mode)")
            except Exception as e2:
                logger.error(f"Failed to load EasyOCR with CPU: {e2}")
                raise

    # =========================
    # PUBLIC API
    # =========================
    async def process_file(
        self,
        file_content: bytes,
        filename: str,
        content_type: str
    ) -> Dict[str, Any]:

        start = time.time()

        if filename.lower().endswith(".pdf"):
            pages = await self._process_pdf(file_content)
        else:
            image = Image.open(io.BytesIO(file_content))
            pages = [await self._ocr_image(image, page_index=1)]

        return {
            "pages": pages,
            "total_pages": len(pages),
            "processing_time": round(time.time() - start, 2)
        }

    # =========================
    # PDF PIPELINE (OPTIMIZED)
    # =========================
    async def _process_pdf(self, file_content: bytes) -> List[Dict[str, Any]]:
        results = []

        # 1️⃣ Try extract text directly (FAST)
        reader = PdfReader(io.BytesIO(file_content))
        extracted_texts = []

        for i, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            extracted_texts.append(text.strip())

        # 2️⃣ Convert PDF to images ONCE
        images = convert_from_bytes(file_content, dpi=200)  # DPI thấp hơn để tăng tốc

        for idx, image in enumerate(images):
            page_no = idx + 1
            text = extracted_texts[idx]

            if len(text) > 50:
                # ✅ Text-based PDF → skip OCR
                logger.info(f"Page {page_no}: extracted text (no OCR)")
                results.append({
                    "page": page_no,
                    "method": "pdf_text",
                    "text": text
                })
            else:
                # ❌ Scan page → OCR
                logger.info(f"Page {page_no}: OCR required")
                ocr_text = await self._ocr_image(
                    image,
                    page_index=page_no
                )
                results.append(ocr_text)

        return results

    # =========================
    # OCR IMAGE (FAST)
    # =========================
    async def _ocr_image(
        self,
        image: Image.Image,
        page_index: int
    ) -> Dict[str, Any]:

        start = time.time()

        # Convert PIL Image to numpy array cho EasyOCR
        import numpy as np
        image_array = np.array(image.convert("RGB"))

        # Chạy OCR
        # EasyOCR trả về list các tuple: (bbox, text, confidence)
        results = self.reader.readtext(image_array)

        # Xử lý kết quả
        text_lines = []
        for (bbox, text, confidence) in results:
            # Chỉ lấy text có confidence > 0.5
            if confidence > 0.5:
                text_lines.append(text)

        # Ghép tất cả text lại
        full_text = "\n".join(text_lines)

        return {
            "page": page_index,
            "method": "easyocr",
            "text": full_text.strip(),
            "time": round(time.time() - start, 2)
        }
