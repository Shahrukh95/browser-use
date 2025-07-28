from bs4 import BeautifulSoup
from typing import Optional
import logging

class SoupParser:
    """A class to parse HTML content using BeautifulSoup."""

    @staticmethod
    def _create_soup(html_content: str) -> Optional[BeautifulSoup]:
        """Create a BeautifulSoup object from HTML content."""
        if not html_content or not isinstance(html_content, str):
            logging.error("Invalid HTML content provided for parsing.")
            return None
        
        try:
            return BeautifulSoup(html_content, 'html.parser')
        except Exception as e:
            logging.error(f"Error parsing HTML: {e}")
            return None


    @staticmethod
    def get_content(html_content: str) -> str:
        """Parse HTML content and return text."""
        soup = SoupParser._create_soup(html_content)
        return soup.get_text(separator='\n\n', strip=True) if soup else 'No Page Content Found'

    @staticmethod
    def get_title(html_content: str) -> str:
        """Extract the title from HTML content."""
        soup = SoupParser._create_soup(html_content)
        title = soup.title.string if soup.title else 'No Title Found'
        return title
    
    
