import os
from flask import Flask
from openai import OpenAI

# Load the OpenAI API key from environment variables
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



if __name__ == "__main__":
    app.run()
