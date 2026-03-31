"""
Flask server — bridges the HTML UI to the Python voice assistant backend.

Endpoints:
  POST /ask              — text → Gemini → text
  POST /vision-upload    — multipart image + prompt → Gemini Vision → text
  POST /vision-b64       — base64 image + prompt → Gemini Vision → text

Run: python server.py
Then open static/voice-assistant-ui.html in your browser.
"""
import os
import base64
import tempfile
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from gpt_module import ask_gpt, ask_vision

app = Flask(__name__, static_folder="static")
CORS(app)


@app.route("/")
def index():
    return send_from_directory("static", "voice-assistant-ui.html")


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    text = (data or {}).get("text", "").strip()
    if not text:
        return jsonify({"error": "No text provided"}), 400
    response = ask_gpt(text)
    return jsonify({"response": response})


@app.route("/vision-upload", methods=["POST"])
def vision_upload():
    """Accept a multipart form with an image file + prompt text."""
    if "image" not in request.files:
        return jsonify({"error": "No image file"}), 400

    prompt   = request.form.get("prompt", "Describe what is in this image briefly.")
    img_file = request.files["image"]

    suffix = os.path.splitext(img_file.filename)[1] or ".jpg"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        img_file.save(tmp.name)
        tmp_path = tmp.name

    try:
        response = ask_vision(prompt, tmp_path)
    finally:
        os.unlink(tmp_path)

    return jsonify({"response": response})


@app.route("/vision-b64", methods=["POST"])
def vision_b64():
    """Accept a base64-encoded image + prompt as JSON."""
    data = request.get_json()
    if not data or "image_b64" not in data:
        return jsonify({"error": "No image_b64 provided"}), 400

    prompt    = data.get("prompt", "Describe what is in this image briefly.")
    image_b64 = data["image_b64"]

    try:
        img_bytes = base64.b64decode(image_b64)
    except Exception:
        return jsonify({"error": "Invalid base64 data"}), 400

    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
        tmp.write(img_bytes)
        tmp_path = tmp.name

    try:
        response = ask_vision(prompt, tmp_path)
    finally:
        os.unlink(tmp_path)

    return jsonify({"response": response})


if __name__ == "__main__":
    print("Starting JARVIS server at http://localhost:5000")
    app.run(port=5000, debug=False)
