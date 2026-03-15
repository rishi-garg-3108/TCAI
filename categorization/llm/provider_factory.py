from django.conf import settings
from .openai_provider import OpenAIProvider
from .ollama_provider import OllamaProvider


def get_llm_provider():

    if settings.LLM_PROVIDER == "openai":
        return OpenAIProvider()

    if settings.LLM_PROVIDER == "ollama":
        return OllamaProvider()

    raise ValueError("Invalid LLM provider")