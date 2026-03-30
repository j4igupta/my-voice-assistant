import os
from dotenv import load_dotenv

load_dotenv()  # FIX: was imported but never called — env vars were always None

PORCUPINE_ACCESS_KEY = os.getenv("PORCUPINE_KEY")
OPENAI_API_KEY       = os.getenv("OPENAI_KEY")   # holds your Gemini API key (kept name for compat)
WAKE_WORD            = "jarvis"
VOSK_MODEL_PATH      = "vosk-model"
PIPER_MODEL          = "en_US-lessac-medium.onnx"
