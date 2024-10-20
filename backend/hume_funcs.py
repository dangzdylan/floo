import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv
from typing import List
from hume import AsyncHumeClient
from hume.expression_measurement.batch import Face, Models
from hume.expression_measurement.batch.types import UnionPredictResult

load_dotenv()
HUME_API_KEY = os.getenv("HUME_API_KEY")

def top_emotions(file):
    client = AsyncHumeClient(api_key=HUME_API_KEY)

    local_filepaths = [
        open("backend/uploaded_audio.wav", mode="rb")
    ]

    # Create configurations for each model you would like to use (blank = default)
    face_config = Face()
    # Create a Models object
    models_chosen = Models(face=face_config)
    
    # Create a stringified object containing the configuration
    stringified_configs = InferenceBaseRequest(models=models_chosen)
    # Start an inference job and print the job_id
    job_id = client.expression_measurement.batch.start_inference_job_from_local_file(
        json=stringified_configs, file=local_filepaths
    )
    print(job_id)


    job_predictions = client.expression_measurement.batch.get_job_predictions(
        id=job_id
    )

    print(job_predictions)

top_emotions("backend/uploaded_audio.wav")