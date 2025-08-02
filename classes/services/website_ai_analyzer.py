from typing import Optional
from pydantic import BaseModel

from classes.web.web_fetch import WebFetch
from classes.processors.soup_parser import SoupParser
from classes.processors.link_processor import LinkProcessor
from classes.models.models import Models
from classes.processors.text_processor import TextProcessor

import logging
import csv
import pandas as pd

class AnalyzeResult(BaseModel):
    """Pydantic model for the result dict of URL analysis."""
    url: str
    cleaned_url: str
    status_code: Optional[int]
    page_load_success: bool
    model_response: str
    extracted_answer: str
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
        self.text_processor = TextProcessor()

        self.max_content_length = 50_000


    def analyze_url(self, url: str, model_name: str, index=1) -> AnalyzeResult:
        """Analyze a URL's content using a model."""

        base_data = {
            "url": url,
            "cleaned_url": "",
            "status_code": None,
            "page_load_success": False,
            "model_response": "",
            "extracted_answer": "",
            "input_tokens": 0,
            "output_tokens": 0,
            "total_cost": 0.0
        }
        
        try:
            # Step 1: Clean and fetch the URL
            cleaned_url = self.link_processor.clean_url(url)
            logging.info(f"{index}) Cleaned URL: {cleaned_url}")
            web_data = self.web_fetch.fetch_url(cleaned_url)

            # If fetch was unsuccessful, try toggling 'www.' prefix
            if web_data['success'] is False:
                logging.warning(f"Failed to fetch {cleaned_url}. Retrying with www prefix.")
                cleaned_url = self.link_processor.toggle_www(cleaned_url)
                logging.info(f"Toggled (www.) URL: {cleaned_url}")
                web_data = self.web_fetch.fetch_url(cleaned_url)

                if web_data['success'] is False:
                    logging.error(f"Failed to fetch {cleaned_url} even after toggling www.")
                else:
                    logging.info(f"Successfully fetched {cleaned_url} after toggling www.")

            logging.info(f"Fetched URL: {web_data['final_url']}")
            logging.info(f"Status Code: {web_data['status_code']}")

            # Extract page content
            text_content = self.soup_parser.get_content(web_data['html_content'])[:self.max_content_length]
            logging.info(f"Page Content: {text_content[:10]}...")
            logging.info(f"Content length: {len(text_content)}")


            # Step 2: Use OpenAI model to analyze content
            model_response, input_tokens, output_tokens, total_cost = self.models.openai_model(
                model_name,
                f"The following is the page content of a website. Check if this is an AI startup or not. Finish your answer with ##### Is AI Startup: [Yes/No]\n\n\n{text_content}"
            )

            # Step 3: Extract answer from model response
            extracted_answer = self.text_processor.extract_answer_from_text(
                searchable_text=model_response,
                question="Is AI Startup",
                valid_answers=["Yes", "No"]
            )

            # logging.info(f"OpenAI Model Response: {model_response}")
            logging.info(f"Is AI Startup: {extracted_answer}")
            logging.info(f"Input Tokens: {input_tokens}")
            logging.info(f"Output Tokens: {output_tokens}")
            logging.info(f"Total Cost: {total_cost}")


            # Create and return Pydantic model
            return AnalyzeResult(
                url=url,
                cleaned_url=cleaned_url,
                status_code=web_data['status_code'],
                page_load_success=web_data['success'],
                model_response=model_response,
                extracted_answer=extracted_answer,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                total_cost=total_cost
            )

        except Exception as e:
            logging.error(f"Error in analyze_url: {str(e)}")
            return AnalyzeResult(**base_data)
        


    def analyze_urls(self, input_csv: str, output_csv: str, start_index: int, stop_index: int, model_name: str) -> None:
        """Analyze multiple URLs using a model."""
        
        df = pd.read_csv(input_csv)

        with open(output_csv, 'w', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file, quoting=csv.QUOTE_ALL)

            if file.tell() == 0:
                writer.writerow(["Name", "Original URL", "Cleaned URL", "Status Code", "Page Load Success", "Model Response", "Extracted Answer", "Input Tokens", "Output Tokens", "Total Cost"])
                file.flush()

            for index, row in df.iterrows():
                if index < start_index:
                    continue
                if index > stop_index:
                    break
                
                url = row['Website']
                result = self.analyze_url(url, model_name, index=index + 1)

                writer.writerow([
                    self.text_processor.csv_text_sanitizer(str(row.get('Startup name'))),
                    self.text_processor.csv_text_sanitizer(result.url),
                    self.text_processor.csv_text_sanitizer(result.cleaned_url),
                    str(result.status_code),
                    str(result.page_load_success),
                    self.text_processor.csv_text_sanitizer(result.model_response),
                    self.text_processor.csv_text_sanitizer(result.extracted_answer),
                    str(result.input_tokens),
                    str(result.output_tokens),
                    str(result.total_cost)
                ])
                file.flush()