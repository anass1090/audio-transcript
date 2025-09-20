import whisperx
import time
import librosa

device = "cpu"  # or "cuda"
audio_file = "audios/test.mp3"
batch_size = 16
compute_type = "float32"

model = whisperx.load_model("small", device=device, compute_type=compute_type)

# load audio manually with librosa (no ffmpeg required)
audio, sr = librosa.load(audio_file, sr=16000, mono=True)

start_time = time.time()
# pass waveform directly
result = model.transcribe(audio, batch_size=batch_size)
end_time = time.time()

alignment_model, align_metadata = whisperx.load_align_model(
    language_code=result["language"], device=device
)

duration_sec = len(audio) / sr
print(f"Loaded audio sr={sr}, duration={duration_sec:.2f}s")

result_aligned = whisperx.align(
    transcript=result["segments"],
    model=alignment_model,
    align_model_metadata=align_metadata,
    audio=audio,
    device=device,
    return_char_alignments=False
)

for word in result_aligned["word_segments"]:
    print(f"[{word['start']:.2f} - {word['end']:.2f}] {word['word'].strip()}")

transcript_text = " ".join([w['word'].strip() for w in result_aligned["word_segments"]])
transcript_text = " ".join(transcript_text.split())

print("\n--- Transcription ---")
print(transcript_text)
