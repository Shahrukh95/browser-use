import re
import logging
from typing import List

class TextProcessor:

    @staticmethod
    def extract_answer_from_text(searchable_text: str, question: str, valid_answers: List[str]) -> str:
        """Extracts an answer from a text that is in the format:
            ##### [Question]: [Answer]

        Args:
            searchable_text (str): The text to search within.
            question (str): The exact question to match (excluding the '##### ' prefix and the ': ' suffix).
            valid_answers (List[str]): Allowed answers to search for (e.g., ["Yes", "No"]).

        Returns:
            str: The matched answer, or "Unknown" if not found.
        """

        try:
            answer_pattern = '|'.join(re.escape(ans) for ans in valid_answers)

            pattern = rf'##### {re.escape(question)}: ({answer_pattern})'
            match = re.search(pattern, searchable_text, re.IGNORECASE)
            
            if match:
                matched_answer = match.group(1).capitalize()
                return matched_answer

            logging.warning(f"Could not find answer for question '{question}' in model response.")
            return "Unknown"

        except Exception as e:
            logging.error(f"Failed to extract answer for question '{question}': {e}")
            return "Unknown"



    def csv_text_sanitizer(self, text: str) -> str:
        """Sanitizes text for CSV output by replacing problematic characters."""

        try:
            sanitized_text = text.replace('\n', ' ').replace('\r', '').replace('\t', ' ').strip()
            return sanitized_text
        except Exception as e:
            logging.error(f"Failed to sanitize text for CSV: {e}")
            return text