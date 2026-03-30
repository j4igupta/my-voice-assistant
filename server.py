from flask import Flask, request, jsonify
from flask_cors import CORS
from gpt_module import ask_gpt

app = Flask(__name__)
CORS(app)

@app.route('/ask', methods=['POST'])
def ask():
    text = request.json.get('text')
    return jsonify({ 'response': ask_gpt(text) })

app.run(port=5000)