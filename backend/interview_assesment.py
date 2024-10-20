from openai import OpenAI
from flask import Flask
from flaskbase import *
import re



def transcript_saver(transcript):
    f = open("transcript.txt", "a")

    for message in transcript:
        f.write(message["role"] + ": " + message["content"])
    f.close()

def assesment_start(transcript_path, resume_path):
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
                You are given an interview transcript.
                Output feedback on the user responses. How could they improve?
                Use specific examples.
            
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

pdf_to_text('backend/Arnav_Khinvasara_resume.pdf')
print(assesment_start('transcript.txt', 'resume.txt'))

'''
def parse_resume(resume):
    # Takes in path to file, writes output file
    client = OpenAI()
    file = client.files.create(
        file=open(resume, "rb"),
        purpose="assistants"
    )
    
    completion = client.beta.assistants.create(
        model="gpt-4o-mini",
        instructions="Return a txt file",
        tools=[{"type": "code_interpreter"}]
    )

    # Upload files and add to vector store
    vector_store = client.beta.vector_stores.create(name="Resumes")
    
    file_paths = [resume]
    file_streams = [open(path, "rb") for path in file_paths]

    completion = client.beta.assistants.update(
        assistant_id=completion.id,
        tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
    )
    file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id, files=file_streams
    )

    # Create thread
    thread = client.beta.threads.create(
        messages=[
            {
            "role": "user",
            "content": "Create a text file named answers.txt with one paragraph for each section in the resume.",
            "attachments": [
                {
                "file_id": file.id,
                "tools": [{"type": "code_interpreter"}, {"type": "file_search"}]
                }
            ]
            }
        ]
    )

    my_run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=completion.id
    )
    
    
    messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=my_run.id))
    message_content = messages[0].content[0].text
    print(messages[0].content[0])
    my_id = str(re.findall("'(.*?)'", str(messages[0].content[0]))[0])

    # Delete thread and files
    client.beta.threads.delete(thread.id)    
    client.files.delete(file.id)
    json = client.files.content(my_id)

    my_file = client.files.content(my_id)
    my_file.stream_to_file("myfilename.txt")
    client.files.delete(my_id)

    return 0
'''