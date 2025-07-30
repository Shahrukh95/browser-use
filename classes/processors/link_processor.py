from urllib.parse import urlparse, urlunparse
import logging

class LinkProcessor():
    """A class to process and clean URLs."""
    
    @staticmethod
    def clean_url(url: str) -> str:
        """Clean and normalize the URL"""

        if not url or not isinstance(url, str):
            logging.error("URL must be a non-empty string")
            raise ValueError("URL must be a non-empty string")
        
        url = url.strip()

        # Ensure the scheme is https
        if not url.startswith(("http://", "https://")):
            url = f"https://{url}"
        elif url.startswith("http://"):
            url = "https://" + url[7:]


        # Parse the URL to ensure it is valid
        try:
            parsed_url = urlparse(url)

            # Ensure the netloc is valid (domain or IP address)
            if not parsed_url.netloc:
                raise ValueError(f"Invalid URL format: {url}")
            
            # There should be a . in the netloc or it should be an IP address
            if ('.' not in parsed_url.netloc and
            not parsed_url.netloc.replace('.', '').replace(':', '').isdigit()):
                raise ValueError(f"Invalid domain in URL: {url}")

            # Rebuild the URL without query and fragment
            cleaned_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, '', '', ''))

            return cleaned_url

        except Exception as e:
            logging.error(f"Failed to parse URL '{url}': {e}")
            raise ValueError(f"Failed to parse URL '{url}': {e}")


    @classmethod
    def toggle_www(cls, url: str) -> str:
        """Toggle 'www.' in the URL. Cleans the URL first."""

        url = cls.clean_url(url)
        
        parsed_url = urlparse(url)

        if "www." in parsed_url.netloc:
            new_netloc = parsed_url.netloc.replace("www.", "", 1)
        else:
            new_netloc = f"www.{parsed_url.netloc}"

        return urlunparse((parsed_url.scheme, new_netloc, parsed_url.path, '', '', ''))



