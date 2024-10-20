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
'''
def top_emotions(file):
    client = AsyncHumeClient(api_key=HUME_API_KEY)

    job_id = await client.expression_measurement.batch.start_inference_job(
        files=[file],
        notify=True,
    )
'''