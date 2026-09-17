import os

from dotenv import load_dotenv
from mlflow import set_tracking_uri
from mlflow.genai import register_prompt
from prompts import SYSTEM_PROMPT

load_dotenv()

MLFLOW_TRACKING_URI = os.getenv(
    "MLFLOW_TRACKING_URI",
    "http://localhost:5001",
)

set_tracking_uri(MLFLOW_TRACKING_URI)

prompt = register_prompt(
    name="fred-personality",
    template=SYSTEM_PROMPT,
    commit_message="Register current FRED personality prompt",
    tags={
        "project": "fred",
        "purpose": "personality",
    },
)

print(f"Registered {prompt.name} version {prompt.version}")
