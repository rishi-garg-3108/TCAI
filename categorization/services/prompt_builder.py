"""
Our goal is to construct a clear, structured, deterministic prompt using the context provided.
The Prompt Builder will:
- Take the structured context from the Context Builder
- Insert that data into a well-designed prompt template
- Ensure the LLM returns structured JSON output
- Restrict the model to valid categories only
"""

import logging

logger = logging.getLogger("transaction_categorizer")


class PromptBuilder:
    """
    Responsible for constructing the LLM prompt using the structured context.
    """

    def build_prompt(self, context: dict) -> str:
        """
        Creates a structured prompt for the LLM using context data.
        """

        try:
            logger.info("Building prompt for LLM")

            # Extracting relevant fields from context
            industry = context["industry"]
            categories = context["categories"]
            historical_examples = context["historical_examples"]
            description = context["transaction_description"]
            vendor = context["vendor"]

            categories_text = "\n".join(f"- {c}" for c in categories)

            prompt = f"""
You are an expert financial assistant responsible for categorizing business transactions.

Industry Context:
{industry}

Valid Chart of Accounts Categories:
{categories_text}

Historical Categorized Transactions:
{historical_examples}

Transaction to Categorize:
Description: {description}
Vendor: {vendor}

Instructions:
- Select the most appropriate category from the valid chart of accounts.
- Use historical examples as guidance.
- Only choose a category from the provided list.

Return ONLY valid JSON in the following format:

{{
"category": "selected category",
"confidence": number between 0 and 1,
"reason": "short explanation for the categorization"
}}

Do not include any text outside the JSON object.
"""

            logger.info("Prompt successfully built")

            return prompt

        except Exception as e:
            logger.error(f"Prompt construction failed: {str(e)}")
            raise
