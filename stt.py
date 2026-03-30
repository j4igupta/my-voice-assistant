import queue
import sounddevice as sd
import json
from vosk import Model, KaldiRecognizer
from config import VOSK_MODEL_PATH

q = queue.Queue()

def callback(indata, frames, time, status):
    q.put(bytes(indata))

def listen():
    model = Model(VOSK_MODEL_PATH)
    recognizer = KaldiRecognizer(model, 16000)

    with sd.RawInputStream(
        samplerate=16000,
        blocksize=8000,
        dtype='int16',
        channels=1,
        callback=callback
    ):
        print("Listening...")

        while True:
            data = q.get()

            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "")

                if text:
                    print("You:", text)
                    return text