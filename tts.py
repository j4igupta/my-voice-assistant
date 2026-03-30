import subprocess
from config import PIPER_MODEL

def speak(text):
    subprocess.run([
        "piper",
        "--model", PIPER_MODEL,
        "--text", text,
        "--output_file", "out.wav"
    ])

    subprocess.run([
        "ffplay",
        "-nodisp",
        "-autoexit",
        "out.wav"
    ])