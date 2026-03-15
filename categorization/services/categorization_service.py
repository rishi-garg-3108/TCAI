""" 
This is central orchestration service that coordinates the entire categorization process.
This service will:
- Receive transaction input
- calls the Build context
- calls Build prompt
- Call the LLM
- Parse the response
- Return structured output

"""

import logging

from categorization.services.context_builder import ContextBuilder
from categorization.services.prompt_builder import PromptBuilder
from categorization.services.response_parser import ResponseParser
# from categorization.llm.openai_provider import OpenAIProvider
from categorization.llm.provider_factory import get_llm_provider



logger = logging.getLogger("transaction_categorizer")


class CategorizationService:
    """
    Orchestrates the transaction categorization pipeline.
    """

    def __init__(self):
        self.context_builder = ContextBuilder()
        self.prompt_builder = PromptBuilder()
        self.llm_provider = get_llm_provider()
        self.response_parser = ResponseParser()

    def categorize_transaction(self, transaction_data: dict) -> dict:
        try:
            logger.info("Starting transaction categorization pipeline")

            # Step 1: Build Context
            print("DEBUG transaction_data:", transaction_data)
            context = self.context_builder.build_context(transaction_data)
            print("DEBUG context:", context)

            # Step 2: Build Prompt
            prompt = self.prompt_builder.build_prompt(context)
            print("DEBUG prompt:", prompt)

            # Step 3: Call LLM
            llm_output = self.llm_provider.generate(prompt)
            print("DEBUG llm_output:", llm_output)

            # Step 4: Parse Response
            parsed_response = self.response_parser.parse(llm_output)
            print("DEBUG parsed_response:", parsed_response)

            return parsed_response

        except Exception as e:
            logger.error(f"Categorization pipeline failed: {str(e)}")
            raise