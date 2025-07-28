import requests
from typing import Optional
import logging


class WebFetch:
    """A class to fetch web content from a given URL."""

    DEFAULT_TIMEOUT = 10
    DEFAULT_HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    @classmethod
    def fetch_url(cls, url:str) -> Optional[dict]:
        """Fetch the content of the URL and return the final URL, status code, and content."""
        
        if not url or not isinstance(url, str):
            logging.error("URL must be a non-empty string")
            return None

        try:
            response = requests.get(url, timeout=cls.DEFAULT_TIMEOUT, headers=cls.DEFAULT_HEADERS)
            response.raise_for_status()  # Raise an error for bad responses
            
            return {
                'final_url': response.url,
                'status_code': response.status_code,
                'html_content': response.text
            }
        
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None
    
