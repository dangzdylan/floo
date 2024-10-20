from flask import Flask, request
from flask_cors import CORS
from deepgram_test import run_deepgram

app = Flask(__name__)
CORS(app)

@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    file = request.files['audio']
    file.save('uploaded_audio.wav')
    run_deepgram('uploaded_audio.wav')

    return "File uploaded successfully", 200

if __name__ == "__main__":
    app.run(debug=True)