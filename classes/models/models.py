import os
import logging
from openai import OpenAI
from dotenv import load_dotenv


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv(os.path.join(BASE_DIR, '.env'))

class Models:

    @staticmethod
    def openai_model(model_name: str, message: str) -> tuple[str, int, int]:
        """Uses OpenAI's *Chat Completions* API to generate a response based on the provided model and message."""
        try:
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            completion = client.chat.completions.create(
                model=model_name,
                messages=[
                    {
                        "role": "user",
                        "content": message
                    }
                ]
            )
            text_response = completion.choices[0].message.content
            input_tokens = completion.usage.prompt_tokens
            output_tokens = completion.usage.completion_tokens

            logging.info(f"OpenAI API called with model: {model_name}, input tokens: {input_tokens}, output tokens: {output_tokens}")

            return text_response, input_tokens, output_tokens
        except Exception as e:
            logging.error(f"OpenAI API error occurred in function openai_model: {str(e)}")
            return f"OpenAI API error occurred: {str(e)}", 0, 0
