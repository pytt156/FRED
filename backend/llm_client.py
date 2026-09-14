import os

from dotenv import load_dotenv
from llm_context import build_llm_input
from openai import OpenAI

load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openrouter")

if LLM_PROVIDER == "openrouter":
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.environ["OPENROUTER_API_KEY"],
    )
    MODEL = os.getenv("OPENROUTER_MODEL", "openrouter/free")

elif LLM_PROVIDER == "openai":
    client = OpenAI(
        api_key=os.environ["OPENAI_API_KEY"],
    )
    MODEL = os.environ["OPENAI_MODEL"]

else:
    raise ValueError(f"Unsupported LLM provider: {LLM_PROVIDER}")


def generate_fred_response(
    room_state: list[str],
    fred_state: list[str],
    display_state: str,
    presence_active: bool,
    trigger: str,
) -> str:
    llm_input = build_llm_input(
        room_state=room_state,
        fred_state=fred_state,
        display_state=display_state,
        presence_active=presence_active,
        trigger=trigger,
    )

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": llm_input,
            }
        ],
    )

    content = response.choices[0].message.content

    if content is None:
        raise ValueError("LLM returned no text content")

    return content
