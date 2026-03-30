"""Quick test — runs camera + Gemini vision without needing the wake word.
Run: python test_vision.py
"""
from vision import capture_image
from gpt_module import ask_vision

print("Testing vision pipeline...")

img = capture_image()

if img:
    response = ask_vision("What is in this image? Describe it briefly.", img)
    print(f"\nGemini says: {response}")
else:
    print("Camera capture failed. Check your camera connection.")
