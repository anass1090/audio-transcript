# import whisperx
# import gc
# import torch

DEVICE = "cuda"  # or "cpu"
BATCH_SIZE = 16
COMPUTE_TYPE = "float16"  # "int8" if GPU memory is low


def transcribe_audio(audio_path: str, model_size: str = "small") -> dict:
    """Transcribe + align audio and return JSON-safe dict."""

    return 'lol'


# def format_result(result: dict) -> dict:
#     """Format WhisperX result into JSON with words + timestamps."""
#     segments_out = []
#     for seg in result["segments"]:
#         words = []
#         if "words" in seg:
#             for w in seg["words"]:
#                 words.append({
#                     "text": w.get("word"),
#                     "start": w.get("start"),
#                     "end": w.get("end")
#                 })
#         segments_out.append({
#             "start": seg.get("start"),
#             "end": seg.get("end"),
#             "text": seg.get("text"),
#             "words": words
#         })

#     return {
#         "language": result.get("language", ""),
#         "segments": segments_out
#     }
