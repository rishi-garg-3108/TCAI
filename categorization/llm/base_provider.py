from abc import ABC, abstractmethod


class BaseLLMProvider(ABC):
    """
    Abstract base class for LLM providers.
    All LLM integrations must implement this interface.
    """

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Generates a response from the LLM based on the given prompt.

        Returns:
            str: Raw response text from the LLM.
        """
        pass