from fastapi import APIRouter, UploadFile, File
from app.Transcription.pipeline import transcribe_audio
import os

router = APIRouter()

@router.get("/health")
async def health_check():
    """Simple health check endpoint."""
    return {"status": "ok"}

@router.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    """Upload audio and return transcript JSON."""
    # Ensure temp dir exists
    os.makedirs("temp", exist_ok=True)

    audio_path = f"temp/{file.filename}"
    with open(audio_path, "wb") as f:
        f.write(await file.read())

    # Run transcription pipeline
    result = transcribe_audio(audio_path)

    # (Optional) cleanup temp file
    os.remove(audio_path)

    return result
