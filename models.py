"""Groq chat-model configuration for the wedding planner."""

import os
from functools import lru_cache

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model


# Load .env without overriding environment variables supplied by deployment platforms.
load_dotenv(override=True)

DEFAULT_MODEL = "openai/gpt-oss-120b"


def get_model_name() -> str:
    """Return the active Groq model ID."""
    return os.getenv("GROQ_MODEL", DEFAULT_MODEL).strip()


@lru_cache(maxsize=4)
def _build_model(model_name: str, temperature: float, max_tokens: int, api_key: str):
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is missing. Add it to your .env file or Streamlit secrets."
        )

    return init_chat_model(
        model=model_name,
        model_provider="groq",
        api_key=api_key,
        temperature=temperature,
        max_tokens=max_tokens,
    )


def get_llm():
    """Create/reuse a model configured from the current environment."""
    return _build_model(
        model_name=get_model_name(),
        temperature=float(os.getenv("GROQ_TEMPERATURE", "0.2")),
        max_tokens=int(os.getenv("GROQ_MAX_TOKENS", "3000")),
        api_key=os.getenv("GROQ_API_KEY", ""),
    )


MODEL_NAME = get_model_name()

# Expose `llm` for modules importing `from models import llm`
try:
    llm = get_llm()
except Exception:
    llm = None


if __name__ == "__main__":
    model = get_llm()
    print("Active Groq model:", get_model_name())
    print(model.invoke("Reply with one short sentence: what color is the sky?").content)
