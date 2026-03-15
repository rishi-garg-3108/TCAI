"""Context builder for categorization service."""

import logging

logger = logging.getLogger("transaction_categorizer")


class ContextBuilder:
    """
    Builds structured context from the validated transaction request.
    This context will later be used by the PromptBuilder.
    """

    def build_context(self, transaction_data: dict) -> dict:
        """
        Constructs the context dictionary used for prompt generation.
        """

        try:
            logger.info("Building context for transaction categorization")

            
            # Below are the important fields to build the context
            company_context = transaction_data["company_context"]
            industry = company_context["industry"]
            chart_of_accounts = company_context["chart_of_accounts"]
            historical_transactions = company_context["historical_transactions"]

            # Formatting historical examples for prompt
            formatted_history = self._format_historical_transactions(
                historical_transactions
            )

            context = {
                "industry": industry,
                "categories": chart_of_accounts,
                "historical_examples": formatted_history,
                "transaction_description": transaction_data["description"],
                "vendor": transaction_data.get("vendor", "")
            }

            logger.info("Context successfully built")

            return context

        except Exception as e:
            logger.error(f"Context building failed: {str(e)}")
            raise

    def _format_historical_transactions(self, historical_transactions: list) -> str:
        """
        Converts historical transactions into formatted examples
        for the prompt.
        """

        try:
            examples = []

            for item in historical_transactions:
                description = item["description"]
                category = item["category"]
                
                
                # Example format used in the prompt
                # "Google Workspace subscription" → Software Subscription
                examples.append(f'"{description}" → {category}')

            return "\n".join(examples)

        except Exception as e:
            logger.error(f"Formatting historical transactions failed: {str(e)}")
            raise