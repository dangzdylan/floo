import os
from flask import Flask, request, send_file
from werkzeug.utils import secure_filename
import PyPDF2
from openai import OpenAI
from resume1 import pdf_to_text
from dotenv import load_dotenv

# Load the OpenAI API key from environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=openai_api_key)


app = Flask(__name__)

interview = []

job_type = []
length = []

@app.route("/interview/setup")
def interview_setup():
    job_type.append(request.json.get("type"))
    length.append(request.json.get("length"))
    interview.append(
        {
            "role": "system", "content": """
            You are acting as an interviewer that asks behavioral questions. 
            The user is applying for a {job_type[0]} role.
            Your job is to ask general behavioral questions that a typical interview would target.
            After each question, you will ask a follow up question about any details important to the job field. This encourages the user to elaborate on his answers and be more through.
            Make sure to be enthuisatic and show that you are an attentive listener!
            The first question you ask will always be "Tell me about yourself".
            """
        }
    )

@app.route("/interview")
def interview_question():
    
    answer = request.json.get("message") # Extract the user's answer

    interview.append({"role": "user", "content": answer})

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[interview]
    )

    # Access the content of the message
    message = completion.choices[0].message.content
    return f"<p>{message}</p>"

@app.route("/interview/followup")
def followup_question():
    pass

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

    pdf_to_text(filepath)


if __name__ == "__main__":
    app.run()
