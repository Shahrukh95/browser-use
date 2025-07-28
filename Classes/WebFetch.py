import requests


class WebFetch:
    """A class to fetch web content from a given URL."""

    
    @staticmethod
    def fetch_url(url):
        """Fetch the content of the URL and return the final URL, status code, and content."""
        
        try:
            response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
            response.raise_for_status()  # Raise an error for bad responses
            
            return {
                'final_url': response.url,
                'status_code': response.status_code,
                'html_content': response.text
            }
        
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    