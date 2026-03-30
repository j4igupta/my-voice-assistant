import subprocess
import os
from config import PIPER_MODEL


def speak(text):
    if not text or not text.strip():
        return

    # FIX: pass text via stdin instead of --text CLI arg.
    # Using --text breaks on quotes, commas, apostrophes, and special chars.
    # Piping via stdin handles any text safely.
    piper_proc = subprocess.Popen(
        ["piper", "--model", PIPER_MODEL, "--output_file", "out.wav"],
        stdin=subprocess.PIPE,
        stderr=subprocess.DEVNULL
    )
    piper_proc.communicate(input=text.encode("utf-8"))

    if os.path.exists("out.wav"):
        subprocess.run(
            ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", "out.wav"]
        )
