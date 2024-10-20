import os
from dotenv import load_dotenv
from deepgram import DeepgramClient, PrerecordedOptions
import json

# The API key we created in step 3
load_dotenv()
DEEPGRAM_API_KEY = os.getenv('DEEPGRAM_API_KEY')


def run_deepgram(PATH_TO_FILE):
    deepgram = DeepgramClient(DEEPGRAM_API_KEY)

    try:
        with open(PATH_TO_FILE, 'rb') as buffer_data:
            payload = { 'buffer': buffer_data }
            options = PrerecordedOptions(
                smart_format=True, model="nova-2", language="en-US"
            )
            response = deepgram.listen.prerecorded.v('1').transcribe_file(payload, options)
            speech_string = response['results']['channels'][0].alternatives[0].transcript
            print(speech_string)
            with open('speech_text_message.json', 'w') as json_file:
                json.dump({"message": speech_string}, json_file, indent=4)
    except FileNotFoundError:
        print(f"Error: The file {PATH_TO_FILE} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
