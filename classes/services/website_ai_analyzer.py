from typing import Optional
from pydantic import BaseModel
from classes.web.web_fetch import WebFetch
from classes.processors.soup_parser import SoupParser
from classes.processors.link_processor import LinkProcessor
from classes.models.models import Models
import logging


class AnalyzeResult(BaseModel):
    """Pydantic model for the result dict of URL analysis."""
    url: str
    status_code: Optional[int]
    model_response: str
    input_tokens: int
    output_tokens: int
    total_cost: float


class WebsiteAIAnalyzer:
    """Analyzes website content using AI models."""

    def __init__(self):
        self.link_processor = LinkProcessor()
        self.web_fetch = WebFetch()
        self.soup_parser = SoupParser()
        self.models = Models()

        self.max_content_length = 50_000


    def analyze_url(self, url: str, model_name: str) -> AnalyzeResult:
        """Analyze a URL's content using a model."""

        base_data = {
            "url": url,
            "status_code": None,
            "model_response": "",
            "input_tokens": 0,
            "output_tokens": 0,
            "total_cost": 0.0
        }
        
        try:
            # Step 1: Clean and fetch the URL
            cleaned_url = self.link_processor.clean_url(url)
            logging.info(f"Cleaned URL: {cleaned_url}")
            web_data = self.web_fetch.fetch_url(cleaned_url)

            logging.info(f"Fetched URL: {web_data['final_url']}")
            logging.info(f"Status Code: {web_data['status_code']}")

            # Extract page content
            text_content = self.soup_parser.get_content(web_data['html_content'])[:self.max_content_length]
            logging.info(f"Page Content: {text_content[:100]}...")
            logging.info(f"Content length: {len(text_content)}")


            # Step 2: Use OpenAI model to analyze content
            model_response, input_tokens, output_tokens, total_cost = self.models.openai_model(
                model_name,
                f"In english, summarize the content of {text_content}"
            )

            logging.info(f"OpenAI Model Response: {model_response}")
            logging.info(f"Input Tokens: {input_tokens}")
            logging.info(f"Output Tokens: {output_tokens}")
            logging.info(f"Total Cost: {total_cost}")


            # Create and return Pydantic model
            return AnalyzeResult(
                url=cleaned_url,
                status_code=web_data['status_code'],
                model_response=model_response,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                total_cost=total_cost
            )

        except Exception as e:
            logging.error(f"Error in analyze_url: {str(e)}")
            return AnalyzeResult(**base_data)