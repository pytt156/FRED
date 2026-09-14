import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)

client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
)

TTS_MODEL = os.getenv("OPENAI_TTS_MODEL", "gpt-4o-mini-tts")
TTS_VOICE = os.getenv("OPENAI_TTS_VOICE", "ash")


def generate_speech(
    text: str,
    output_path: str = "fred_speech.wav",
) -> Path:
    path = Path(output_path)

    with client.audio.speech.with_streaming_response.create(
        model=TTS_MODEL,
        voice=TTS_VOICE,
        input=text,
        instructions=("Speak in a dry sarcastic tone. Sound mildly inconvenienced."),
        response_format="wav",
    ) as response:
        response.stream_to_file(path)

    return path
