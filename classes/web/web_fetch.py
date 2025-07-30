import requests
from typing import Optional, TypedDict
import logging


class FetchResult(TypedDict):    
    final_url: Optional[str]
    status_code: Optional[int]
    html_content: Optional[str]
    success: bool


class WebFetch:
    """A class to fetch web content from a given URL."""

    DEFAULT_TIMEOUT = 10
    DEFAULT_HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    @classmethod
    def fetch_url(cls, url: str) -> FetchResult:
        """Fetch the content of the URL and return the final URL, status code, and content."""
        
        if not url or not isinstance(url, str):
            logging.error("URL must be a non-empty string")
            return {
                'final_url': None,
                'status_code': None,
                'html_content': None,
                'success': False
            }

        try:
            response = requests.get(url, timeout=cls.DEFAULT_TIMEOUT, headers=cls.DEFAULT_HEADERS)
            
            return {
                'final_url': response.url,
                'status_code': response.status_code,
                'html_content': response.text,
                'success': response.ok
            }
        
        except requests.RequestException as e:
            logging.error(f"Error fetching {url}: {e}")
            return {
                'final_url': url,
                'status_code': None,
                'html_content': None,
                'success': False
            }
