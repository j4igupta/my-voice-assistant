"""
Flask server — bridges the HTML UI to the Python voice assistant backend.

Run: python server.py
Then open static/voice-assistant-ui.html in your browser.
"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from gpt_module import ask_gpt, ask_vision
from vision import capture_image
import os

app = Flask(__name__, static_folder="static")
CORS(app)


@app.route("/")
def index():
    return send_from_directory("static", "voice-assistant-ui.html")


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "No text provided"}), 400

    response = ask_gpt(text)
    return jsonify({"response": response})


@app.route("/vision", methods=["POST"])
def vision():
    """Trigger camera capture + vision analysis from the UI."""
    data = request.get_json()
    prompt = data.get("prompt", "Describe what you see briefly.")

    image_path = capture_image()
    if not image_path:
        return jsonify({"error": "Camera capture failed"}), 500

    response = ask_vision(prompt, image_path)
    return jsonify({"response": response, "image": image_path})


if __name__ == "__main__":
    print("Starting server at http://localhost:5000")
    app.run(port=5000, debug=False)
