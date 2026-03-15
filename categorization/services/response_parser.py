""" response parser will keep the output within the defined structure of output"""

import json
import logging

logger = logging.getLogger("transaction_categorizer")


class ResponseParser:
    """
    Parses and validates the LLM response to ensure deterministic structured output.
    """

    REQUIRED_FIELDS = ["category", "confidence", "reason"]

    def parse(self, llm_output: str) -> dict:
        """
        Parses the raw LLM output and ensures required structure.

        Args:
            llm_output (str): Raw response text from LLM.

        Returns:
            dict: Parsed structured response.
        """

        try:
            logger.info("Parsing LLM response")

            # Strip markdown code fences if present
            cleaned = llm_output.strip()
            if cleaned.startswith("```"):
                cleaned = cleaned.split("```")[1]
                if cleaned.startswith("json"):
                    cleaned = cleaned[4:]
                cleaned = cleaned.strip()

            parsed = json.loads(cleaned)

            self._validate(parsed)

            return parsed

        except json.JSONDecodeError:
            logger.error("LLM returned invalid JSON")
            raise ValueError("Invalid JSON returned from LLM")

        except Exception as e:
            logger.error(f"Response parsing failed: {str(e)}")
            raise

    def _validate(self, parsed: dict):
        """
        Validates required fields in the parsed output.
        """

        for field in self.REQUIRED_FIELDS:
            # Raising error if any of the field is missing
            if field not in parsed:
                raise ValueError(f"Missing required field: {field}")

        # Checking if the values have the correct type
        if not isinstance(parsed["confidence"], (int, float)):
            raise ValueError("Confidence must be numeric")

        if parsed["confidence"] < 0 or parsed["confidence"] > 1:
            raise ValueError("Confidence must be between 0 and 1")