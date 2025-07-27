from urllib.parse import urlparse, urlunparse


class LinkProcessor():
    def __init__(self):
        pass

    @staticmethod
    def clean_url(url: str) -> str:
        """Clean and normalize the URL"""

        if not url or not isinstance(url, str):
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
            not parsed_url.netloc.replace('.', '').isdigit()):
                raise ValueError(f"Invalid domain in URL: {url}")

            # Rebuild the URL without query and fragment
            cleaned_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, '', '', ''))

            return cleaned_url

        except Exception as e:
            raise ValueError(f"Failed to parse URL '{url}': {e}")


    @staticmethod
    def toggle_www(url: str) -> str:
        """Toggle 'www.' in the URL. Cleans the URL first."""

        url = LinkProcessor.clean_url(url)

        if not url or not isinstance(url, str):
            raise ValueError("URL must be a non-empty string")

        if "www." in url:
            return url.replace("www.", "", 1)  # Remove 'www.' only once
        else:
            parts = url.split("://")
            if len(parts) == 2:
                return f"{parts[0]}://www.{parts[1]}"  # Add 'www.'
        
        return f"www.{url}"
