import pvporcupine
import sounddevice as sd
import numpy as np
import threading
from config import PORCUPINE_ACCESS_KEY, WAKE_WORD


def listen_for_wake():
    porcupine = pvporcupine.create(
        access_key=PORCUPINE_ACCESS_KEY,
        keywords=[WAKE_WORD]
    )

    # FIX: use an Event instead of sd.sleep(100000) — reliably stops the
    # stream the instant the wake word fires, no matter when that happens.
    detected = threading.Event()

    def callback(indata, frames, time, status):
        pcm = np.frombuffer(indata, dtype=np.int16)
        keyword_index = porcupine.process(pcm)
        if keyword_index >= 0:
            print("Wake word detected!")
            detected.set()
            raise sd.CallbackStop()

    with sd.InputStream(
        samplerate=porcupine.sample_rate,
        blocksize=porcupine.frame_length,  # FIX: match porcupine's required frame size
        channels=1,
        dtype='int16',
        callback=callback
    ):
        print(f"Listening for wake word: '{WAKE_WORD}'...")
        detected.wait()  # blocks until wake word fires, no timeout

    porcupine.delete()  # FIX: clean up native resource
