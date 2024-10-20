from openai import OpenAI
from flask import Flask

import re


# TODO:
#       fix arguments + write output to flask
#       return smth if file failed

def parse_resume(resume):
    # Takes in path to file, writes output file
    client = OpenAI(api_key="xxxx")
    file = client.files.create(
        file=open(resume, "rb"),
        purpose="assistants"
    )
    
    completion = client.beta.assistants.create(
        model="gpt-4o-mini",
        instructions="Return a json file",
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
