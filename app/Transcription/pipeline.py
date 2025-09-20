import whisperx
import librosa
import time
import subprocess
import numpy as np

DEVICE = "cpu"  # or "cuda"
BATCH_SIZE = 16
COMPUTE_TYPE = "float32"


def load_models(model_size: str = "small", device: str = DEVICE):
    asr_model = whisperx.load_model(model_size, device=device, compute_type=COMPUTE_TYPE)
    alignment_model, align_metadata = whisperx.load_align_model(
        language_code="en",
        device=device
    )
    return asr_model, alignment_model, align_metadata


def load_audio_ffmpeg(path: str, sr: int = 16000) -> np.ndarray:
    cmd = [
        "ffmpeg", "-i", path,
        "-f", "s16le", "-ac", "1", "-ar", str(sr), "-"
    ]
    out = subprocess.run(cmd, capture_output=True, check=True).stdout
    audio = np.frombuffer(out, np.int16).astype(np.float32) / 32768.0
    return audio


def transcribe_audio(audio_path: str,
                     asr_model,
                     alignment_model,
                     align_metadata,
                     device: str = DEVICE) -> dict:
    audio = load_audio_ffmpeg(audio_path, sr=16000)
    sr = 16000

    start_time = time.time()
    result = asr_model.transcribe(audio)
    end_time = time.time()
    print(f"Transcription took {end_time - start_time:.2f} sec")

    if result["language"] != align_metadata["language"]:
        alignment_model, align_metadata = whisperx.load_align_model(
            language_code=result["language"], device=device
        )

    result_aligned = whisperx.align(
        transcript=result["segments"],
        model=alignment_model,
        align_model_metadata=align_metadata,
        audio=audio,
        device=device,
        return_char_alignments=False
    )

    # flatten into word list
    words_out = []
    i = 0
    for seg in result_aligned["segments"]:
        if "words" in seg:
            for w in seg["words"]:
                words_out.append({
                    "i": i,
                    "word": w.get("word", "").strip(),
                    "start": w.get("start"),
                    "end": w.get("end")
                })
                i += 1

    return {
        "language": result_aligned.get("language", result.get("language", "")),
        "words": words_out
    }


