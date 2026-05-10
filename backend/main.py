from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services.ai_service import ai_service
from services.pdf_service import extract_text_from_pdf

app = FastAPI(title="AI Text Summarizer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextSummaryRequest(BaseModel):
    text: str
    max_length: int = 150
    min_length: int = 30

@app.post("/summarize/text")
async def summarize_text(request: TextSummaryRequest):
    if not request.text or len(request.text.strip()) == 0:
        raise HTTPException(status_code=400, detail="No text provided.")
    
    try:
        summary = ai_service.summarize(request.text, request.max_length, request.min_length)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/summarize/pdf")
async def summarize_pdf(file: UploadFile = File(...), max_length: int = Form(150), min_length: int = Form(30)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF.")
    
    try:
        contents = await file.read()
        extracted_text = extract_text_from_pdf(contents)
        if not extracted_text:
            raise HTTPException(status_code=400, detail="Could not extract text from PDF.")
            
        summary = ai_service.summarize(extracted_text, max_length, min_length)
        return {"summary": summary, "extracted_text_preview": extracted_text[:200] + "..."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def health_check():
    return {"status": "ok"}
