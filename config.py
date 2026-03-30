import os
from dotenv import load_dotenv

PORCUPINE_ACCESS_KEY = os.getenv("PORCUPINE_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_KEY")
WAKE_WORD = "jarvis"

VOSK_MODEL_PATH = "vosk-model"
PIPER_MODEL = "en_US-lessac-medium.onnx"