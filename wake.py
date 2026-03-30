import pvporcupine
import sounddevice as sd
import numpy as np
from config import PORCUPINE_ACCESS_KEY, WAKE_WORD

def listen_for_wake():
    porcupine = pvporcupine.create(
        access_key=PORCUPINE_ACCESS_KEY,
        keywords=[WAKE_WORD]
    )

    def callback(indata, frames, time, status):
        pcm = np.frombuffer(indata, dtype=np.int16)
        keyword_index = porcupine.process(pcm)

        if keyword_index >= 0:
            print("Wake word detected!")
            raise sd.CallbackStop()

    with sd.InputStream(
        samplerate=porcupine.sample_rate,
        channels=1,
        dtype='int16',
        callback=callback
    ):
        print("Listening for wake word...")
        sd.sleep(100000)