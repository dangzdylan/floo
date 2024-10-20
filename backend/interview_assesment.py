from openai import OpenAI
from flask import Flask
from flaskbase import *
import json
import re
load_dotenv(dotenv_path='/backend')
openai_api_key = os.getenv(OPENAI_API_KEY)


def transcript_saver(transcript):
    f = open("transcript.txt", "a")

    for message in transcript:
        f.write(message["role"] + ": " + message["content"])
    f.close()

def assessment_start(transcript_path, resume_path):
    # Takes in path to transcript txt file and resume txt file
    # Returns feedback text
    client = OpenAI(api_key=openai_api_key)
    
    # Create files for assistant
    transcript = client.files.create(
        file=open(transcript_path, "rb"),
        purpose="assistants"
    )
    resume = client.files.create(
        file=open(resume_path, "rb"),
        purpose="assistants"
    )
    assistant = client.beta.assistants.create(
        model="gpt-4o-mini",
        instructions="Output feedback according to the two given files.",
        tools=[{"type": "code_interpreter"}, {"type": "file_search"}]
    )

    # Upload files and add to vector store
    transcript_vector = client.beta.vector_stores.create(name="Transcript")
    resume_vector = client.beta.vector_stores.create(name="Resume")

    file_paths = [transcript_path]
    file_streams = [open(path, "rb") for path in file_paths]

    assistant = client.beta.assistants.update(
        assistant_id=assistant.id,
        tool_resources={"file_search": {"vector_store_ids": [transcript_vector.id]}},
    )
    client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=transcript_vector.id, files=file_streams
    )

    file_paths = [resume_path]
    file_streams = [open(path, "rb") for path in file_paths]

    client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=resume_vector.id, files=file_streams
    )

    # Create thread
    thread = client.beta.threads.create(
        messages=[
            {
            "role": "user",
            "content": """
                I have attatched a transcript file. Now I will attatch a resume
                file.
            
            """,
            "attachments": [
                {
                "file_id": transcript.id,
                "tools": [{"type": "code_interpreter"}, {"type": "file_search"}]
                }
            ]
            },
            {
                "role": "user",
            "content": """
                You are given both an interview transcript and a resume.
                Tell the user feedback on the user responses. How could they improve?
                Use specific examples. Be concise and do not write much.
            
            """,
            "attachments": [
                {
                "file_id": resume.id,
                "tools": [{"type": "code_interpreter"}, {"type": "file_search"}]
                }
            ]
            }
        ]
    )
    
    run0 = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant.id
    )

    messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run0.id))
    
    message2 = client.beta.threads.messages.create(
        thread.id,
        role="user",
        content="""
                For every answer given by the user in the interview, output an improved answer.
                Do not output anything else. Be very concise and do not write a lot for every answer.
                """,
    )

    run1 = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant.id
    )

    messages2 = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run1.id))


    message3 = client.beta.threads.messages.create(
        thread.id,
        role="user",
        content="""
                Output a single number, nothing else, representing the rating of the user's interview performance.
                """,
    )

    run2 = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant.id
    )

    messages3 = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run2.id))

    # delete files, thread, assistant
    
    client.beta.threads.delete(thread.id) 
    client.beta.assistants.delete(assistant.id)   
    
    client.files.delete(transcript.id)
    client.files.delete(resume.id)


    with open(transcript_path, "r") as text_file:
        transcript_string = text_file.read()
    
    y = {"interview": transcript_string,
        "better_answers": messages2[0].content[0].text.value,
        "feedback": messages[0].content[0].text.value,
        "score": messages3[0].content[0].text.value
        }

    with open("backend/data.json",'r+') as file:
        file_data = json.load(file)
        file_data["previous_interviews"].append(y)
        file.seek(0)
        json.dump(file_data, file, indent = 4)

    return y


def obtain_rating(transcript_path, resume_path):
    # Takes in path to transcript txt file and resume txt file
    # Returns feedback text
    client = OpenAI(api_key=openai_api_key)
    
    # Create files for assistant
    transcript = client.files.create(
        file=open(transcript_path, "rb"),
        purpose="assistants"
    )
    resume = client.files.create(
        file=open(resume_path, "rb"),
        purpose="assistants"
    )
    assistant = client.beta.assistants.create(
        model="gpt-4o-mini",
        instructions="Output a single number from one to ten according to the given interview transcript.",
        tools=[{"type": "code_interpreter"}, {"type": "file_search"}]
    )

    # Upload files and add to vector store
    transcript_vector = client.beta.vector_stores.create(name="Transcript")
    resume_vector = client.beta.vector_stores.create(name="Resume")

    file_paths = [transcript_path]
    file_streams = [open(path, "rb") for path in file_paths]

    assistant = client.beta.assistants.update(
        assistant_id=assistant.id,
        tool_resources={"file_search": {"vector_store_ids": [transcript_vector.id]}},
    )
    client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=transcript_vector.id, files=file_streams
    )

    file_paths = [resume_path]
    file_streams = [open(path, "rb") for path in file_paths]

    client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=resume_vector.id, files=file_streams
    )

    # Create thread
    thread = client.beta.threads.create(
        messages=[
            {
            "role": "user",
            "content": """
                You are given an interview transcript.
                Only output a single number from 1-10 based on their rating.
                Do not output anything else.
            """,
            "attachments": [
                {
                "file_id": transcript.id,
                "tools": [{"type": "code_interpreter"}, {"type": "file_search"}]
                }
            ]
            }
        ]
    )
    
    run0 = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant.id
    )

    messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run0.id))
    
    # delete files, thread, assistant
    
    client.beta.threads.delete(thread.id) 
    client.beta.assistants.delete(assistant.id)   
    
    client.files.delete(transcript.id)
    client.files.delete(resume.id)

    return messages[0].content[0].text.value


