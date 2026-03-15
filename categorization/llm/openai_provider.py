"""setup for openai"""

import logging
from openai import OpenAI
from django.conf import settings

from .base_provider import BaseLLMProvider

logger = logging.getLogger("transaction_categorizer")


class OpenAIProvider(BaseLLMProvider):
    """
    OpenAI implementation of the LLM provider.
    """

    def __init__(self):
        print("OPENAI KEY:", settings.OPENAI_API_KEY[:10])
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def generate(self, prompt: str) -> str:

        try:
            response = self.client.chat.completions.create(
                model=settings.MODEL_NAME,
                temperature=0,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            if not response or not response.choices:
                raise ValueError("Empty response from OpenAI")

            content = response.choices[0].message.content

            if content is None:
                raise ValueError("OpenAI returned empty message content")

            print("FULL OPENAI RESPONSE:", response) # Debugging line to inspect the full response
            return content

        except Exception as e:
            logger.error(f"OpenAI API call failed: {str(e)}")
            raise