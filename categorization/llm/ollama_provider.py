""" Setup for ollama"""

import logging
import ollama
from django.conf import settings
from .base_provider import BaseLLMProvider

logger = logging.getLogger("transaction_categorizer")


class OllamaProvider(BaseLLMProvider):

    def generate(self, prompt: str) -> str:

        try:
            logger.info("Sending prompt to Ollama")

            response = ollama.chat(
                model=settings.OLLAMA_MODEL,
                messages=[{"role": "user", "content": prompt}]
            )

            logger.info("Received response from Ollama")

            return response["message"]["content"]

        except Exception as e:
            logger.error(f"Ollama call failed: {str(e)}")
            raise