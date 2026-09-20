import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from piper import PiperVoice

load_dotenv(override=True)

MODEL_MODE = os.getenv("MODEL_MODE", "openai")

OPENAI_TTS_MODEL = os.getenv("OPENAI_TTS_MODEL", "gpt-4o-mini-tts")
OPENAI_TTS_VOICE = os.getenv("OPENAI_TTS_VOICE", "ash")

BASE_DIR = Path(__file__).resolve().parent

DEFAULT_PIPER_VOICE_PATH = BASE_DIR / "voices" / "en_US-hfc_male-medium.onnx"

PIPER_VOICE_PATH = Path(os.getenv("PIPER_VOICE_PATH") or DEFAULT_PIPER_VOICE_PATH)

openai_client = None
piper_voice = None


def generate_openai_speech(text: str) -> tuple[bytes, int]:
    global openai_client

    if openai_client is None:
        openai_client = OpenAI(
            api_key=os.environ["OPENAI_API_KEY"],
        )

    response = openai_client.audio.speech.create(
        model=OPENAI_TTS_MODEL,
        voice=OPENAI_TTS_VOICE,
        input=text,
        instructions=("Speak in a dry sarcastic tone. Sound mildly inconvenienced."),
        response_format="pcm",
    )

    return response.content, 24000


def generate_piper_speech(text: str) -> tuple[bytes, int]:
    global piper_voice

    if piper_voice is None:
        if not PIPER_VOICE_PATH.exists():
            raise FileNotFoundError(f"Piper voice model not found: {PIPER_VOICE_PATH}")

        piper_voice = PiperVoice.load(str(PIPER_VOICE_PATH))

    audio_parts = []
    sample_rate = None

    for chunk in piper_voice.synthesize(text):
        if sample_rate is None:
            sample_rate = chunk.sample_rate

        audio_parts.append(chunk.audio_int16_bytes)

    if sample_rate is None:
        raise RuntimeError("Piper returned no audio")

    return b"".join(audio_parts), sample_rate


def generate_speech(text: str) -> tuple[bytes, int]:
    if MODEL_MODE == "free":
        return generate_piper_speech(text)

    if MODEL_MODE == "openai":
        return generate_openai_speech(text)

    raise ValueError(f"Unsupported MODEL_MODE: {MODEL_MODE}")


if __name__ == "__main__":
    audio_bytes, sample_rate = generate_speech("Wonderful. Another human interaction.")

    print(type(audio_bytes))
    print(len(audio_bytes))
    print(f"Sample rate: {sample_rate}")
