from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging

from ocr_service import OCRService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="OCR API with PaddleOCR", version="2.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ocr_service = OCRService()


@app.get("/")
async def root():
    return {"message": "OCR API với PaddleOCR", "status": "running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "model_loaded": True}


@app.post("/ocr")
async def ocr(file: UploadFile = File(...)):
    try:
        content = await file.read()
        
        if not content:
            raise HTTPException(status_code=400, detail="File rỗng")
        
        result = await ocr_service.process_file(
            file_content=content,
            filename=file.filename,
            content_type=file.content_type
        )

        return JSONResponse(content={
            "success": True,
            "filename": file.filename,
            **result
        })
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Lỗi xử lý file: {str(e)}")
