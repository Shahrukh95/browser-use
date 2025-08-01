from classes import LinkProcessor, SoupParser, WebFetch, Models
from classes.services.website_ai_analyzer import WebsiteAIAnalyzer
import pandas as pd
import logging

logging.basicConfig(
    filename='startups.log',
    filemode='w',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    analyzer = WebsiteAIAnalyzer()

    # analysize input URLs
    analyzer.analyze_urls("startups.csv", "output.csv", 15, 19, "gpt-4.1-mini")
    
    # logging.info(f"Analysis Result: {result.model_dump()}")


if __name__ == "__main__":
    main()



