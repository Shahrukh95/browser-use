import os
import logging
from openai import OpenAI
from dotenv import load_dotenv

from .model_pricing import ModelPricing


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv(os.path.join(BASE_DIR, '.env'))

class Models:

    @classmethod
    def openai_model(cls, model_name: str, message: str) -> tuple[str, int, int, float]:
        """Uses OpenAI's *Chat Completions* API to generate a response based on the provided model and message."""
        try:
            client = OpenAI(api_key=os.getenv("CUSTOM_OPENAI_API_KEY"))
            completion = client.chat.completions.create(
                model=model_name,
                messages=[
                    {
                        "role": "user",
                        "content": message
                    }
                ]
            )
            response = completion.choices[0].message.content
            input_tokens = completion.usage.prompt_tokens
            output_tokens = completion.usage.completion_tokens
            total_cost = ModelPricing.calculate_cost(model_name, input_tokens, output_tokens)

            return response, input_tokens, output_tokens, total_cost
        
        except Exception as e:
            logging.error(f"OpenAI API error occurred in function openai_model: {str(e)}")
            return f"OpenAI API error occurred", 0, 0, float(0)

