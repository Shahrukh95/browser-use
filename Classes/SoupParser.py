from bs4 import BeautifulSoup

class SoupParser:
    """A class to parse HTML content using BeautifulSoup."""

    @staticmethod
    def _create_soup(html_content):
        """Create a BeautifulSoup object from HTML content."""
        try:
            return BeautifulSoup(html_content, 'html.parser')
        except Exception as e:
            print(f"Error parsing HTML: {e}")
            return None

    @staticmethod
    def get_content(html_content):
        """Parse HTML content and return text."""
        soup = SoupParser._create_soup(html_content)
        return soup.get_text(separator='\n\n', strip=True) if soup else 'No Page Content Found'

    @staticmethod
    def get_title(html_content):
        """Extract the title from HTML content."""
        soup = SoupParser._create_soup(html_content)
        title = soup.title.string if soup.title else 'No Title Found'
        return title
    
    
