from fastapi import FastAPI, UploadFile, File
from app.Transcription.pipeline import transcribe_audio
from app.API.routes import router as api_router

app = FastAPI(title="Voice Diary Transcription API")
app.include_router(api_router)

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):

    audio_path = f"audios/{file.filename}"
    with open(audio_path, "wb") as f:
        f.write(await file.read())

    result = transcribe_audio(audio_path)

    return result
