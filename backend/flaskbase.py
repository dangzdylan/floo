import os
from flask import Flask, request, send_file, jsonify
from werkzeug.utils import secure_filename
import PyPDF2
from openai import OpenAI
from resume1 import pdf_to_text
from dotenv import load_dotenv
from flask_cors import CORS
from deepgram_test import run_deepgram
from text_to_speech import text_to_speech

# Load the OpenAI API key from environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=openai_api_key)

app = Flask(__name__)
CORS(app)

interview = []

length = []
first_question = [False]

@app.route("/interview/setup", methods=["POST"])
def interview_setup():
    length.append(request.json.get("length"))
    interview.append(
        {
            "role": "system", "content": """
            You are acting as an interviewer that asks behavioral questions. 
            The user is applying for a software engineering role.
            Your job is to ask general behavioral questions that a typical interview would target.
            After each question, you will ask a follow up question about any details important to the job field. This encourages the user to elaborate on his answers and be more through.
            Make sure to be enthuisatic and show that you are an attentive listener!
            The first question you ask will always be "Tell me about yourself".
            """
        }
    )

@app.route("/interview")
def interview_question():

    length[0] -= 1

    if (first_question[0]):
        answer = request.json.get("message") # Extract the user's answer
        interview.append({"role": "user", "content": answer})

    first_question[0] = True

    interview.append({"role": "system", "content": "Give a kind short response if the user has answered a question. Then ask another one."})

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[interview]
    )

    # Access the content of the message
    message = completion.choices[0].message.content
    return jsonify({"response": message})

@app.route("/interview/followup")
def followup_question():
    
    answer = request.json.get("message") # Extract the user's answer

    interview.append(
        {"role": "user", "content": answer},
        {"role": "system", "content": "You will recieve an answer to the question. Respond with a follow up question that encourages the user to elaborate on vague details."}
    )

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[interview]
    )

    message = completion.choices[0].message.content
    if (length[0] > 0):
        return jsonify({"response": message, "continue": True})
    else:
        return jsonify({"response": message, "continue": False})

@app.route("/interview/save")
def interview_save():
    answer = request.json.get("message") # Extract the user's answer

    interview.append(
        {"role": "user", "content": answer}
    )
    return jsonify({"reponse": "Thank you"})

@app.route("/resumeParser", methods=["POST"])
def resumeParser():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
   
    if file.filename == '':
        return "No selected file", 400
    # Secure the filename
    filename = secure_filename(file.filename)
    # Save the file temporarily
    filepath = f'./{filename}'
    file.save(filepath)

    pdf_to_text(filepath)

    return "File saved successfully"

@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    file = request.files['audio']
    file.save('uploaded_audio.wav')
    run_deepgram('uploaded_audio.wav')

    return "File uploaded successfully", 200

@app.route('/text_to_speech', methods=['POST'])
def handle_text_to_speech() :
    data = request.json
    text = data.get('text', '')
    
    # Generate the speech file
    audio_file = text_to_speech(text)
    
    if audio_file:
        return send_file(audio_file, mimetype="audio/wav")
    else:
        return jsonify({"error": "Failed to generate audio"}), 500



if __name__ == "__main__":
    app.run()