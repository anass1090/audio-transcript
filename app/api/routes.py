from fastapi import APIRouter, UploadFile, File
import tempfile, os, shutil
from app.transcription.pipeline import load_models, transcribe_audio

router = APIRouter()

asr_model, alignment_model, align_metadata = load_models()

@router.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
        shutil.copyfileobj(file.file, tmp)
        audio_path = tmp.name

    try:
        result = transcribe_audio(audio_path, asr_model, alignment_model, align_metadata)
    finally:
        os.remove(audio_path)

    return result
