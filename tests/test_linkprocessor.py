import unittest
import sys
import os

# Add the parent directory to the path to import Classes
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from Classes.LinkProcessor import LinkProcessor


class TestLinkProcessor(unittest.TestCase):
    
    def setUp(self):
        self.processor = LinkProcessor()
    
    def test_clean_url_with_https(self):
        """Test clean_url with https URL"""
        url = "https://example.com/path?query=123#fragment"
        result = LinkProcessor.clean_url(url)
        self.assertEqual(result, "https://example.com/path")
    
    def test_clean_url_without_scheme(self):
        """Test clean_url without scheme - should add https"""
        url = "example.com/path?query=123"
        result = LinkProcessor.clean_url(url)
        self.assertEqual(result, "https://example.com/path")
    
    def test_clean_url_with_http(self):
        """Test clean_url with http - should convert to https"""
        url = "http://example.com/path"
        result = LinkProcessor.clean_url(url)
        self.assertEqual(result, "https://example.com/path")
    
    def test_clean_url_removes_query_and_fragment(self):
        """Test that query parameters and fragments are removed"""
        url = "https://example.com/path?query=123&other=456#section"
        result = LinkProcessor.clean_url(url)
        self.assertEqual(result, "https://example.com/path")
    
    def test_clean_url_with_empty_string(self):
        """Test clean_url with empty string - should raise ValueError"""
        with self.assertRaises(ValueError):
            LinkProcessor.clean_url("")
    
    def test_clean_url_with_none(self):
        """Test clean_url with None - should raise ValueError"""
        with self.assertRaises(ValueError):
            LinkProcessor.clean_url(None)
    
    def test_clean_url_with_non_string(self):
        """Test clean_url with non-string input"""
        with self.assertRaises(ValueError):
            LinkProcessor.clean_url(123)
    
    def test_clean_url_with_invalid_url(self):
        """Test clean_url with invalid URL format"""
        with self.assertRaises(ValueError):
            LinkProcessor.clean_url("not-a-valid-url")

    # New comprehensive tests
    def test_clean_url_with_ipv4_address(self):
        """Test clean_url with IPv4 address"""
        url = "192.168.1.1/path?query=123"
        result = LinkProcessor.clean_url(url)
        self.assertEqual(result, "https://192.168.1.1/path")

    def test_clean_url_with_ipv4_and_port(self):
        """Test clean_url with IPv4 address and port"""
        url = "http://192.168.1.1:8080/api"
        result = LinkProcessor.clean_url(url)
        self.assertEqual(result, "https://192.168.1.1:8080/api")

    def test_clean_url_with_subdomain(self):
        """Test clean_url with subdomain"""
        url = "api.example.com/v1/users"
        result = LinkProcessor.clean_url(url)
        self.assertEqual(result, "https://api.example.com/v1/users")

    def test_clean_url_with_port(self):
        """Test clean_url with port number"""
        url = "https://example.com:8443/secure"
        result = LinkProcessor.clean_url(url)
        self.assertEqual(result, "https://example.com:8443/secure")

    def test_clean_url_with_trailing_slash(self):
        """Test clean_url with trailing slash"""
        url = "https://example.com/"
        result = LinkProcessor.clean_url(url)
        self.assertEqual(result, "https://example.com/")

    def test_clean_url_with_deep_path(self):
        """Test clean_url with deep path structure"""
        url = "example.com/api/v1/users/123/posts"
        result = LinkProcessor.clean_url(url)
        self.assertEqual(result, "https://example.com/api/v1/users/123/posts")

    def test_clean_url_with_whitespace(self):
        """Test clean_url with leading/trailing whitespace"""
        url = "  https://example.com/path  "
        result = LinkProcessor.clean_url(url)
        self.assertEqual(result, "https://example.com/path")

    def test_clean_url_root_domain_only(self):
        """Test clean_url with root domain only"""
        url = "example.com"
        result = LinkProcessor.clean_url(url)
        self.assertEqual(result, "https://example.com")

    def test_clean_url_with_special_characters_in_path(self):
        """Test clean_url with special characters in path"""
        url = "example.com/path-with_special.chars/123"
        result = LinkProcessor.clean_url(url)
        self.assertEqual(result, "https://example.com/path-with_special.chars/123")

    # Toggle www tests
    def test_toggle_www_add_www(self):
        """Test adding www to URL without it"""
        url = "https://example.com/path"
        result = LinkProcessor.toggle_www(url)
        self.assertEqual(result, "https://www.example.com/path")

    def test_toggle_www_remove_www(self):
        """Test removing www from URL with it"""
        url = "https://www.example.com/path"
        result = LinkProcessor.toggle_www(url)
        self.assertEqual(result, "https://example.com/path")

    def test_toggle_www_with_subdomain(self):
        """Test toggle_www with existing subdomain"""
        url = "https://api.example.com/path"
        result = LinkProcessor.toggle_www(url)
        self.assertEqual(result, "https://www.api.example.com/path")

    def test_toggle_www_with_ip_address(self):
        """Test toggle_www with IP address"""
        url = "192.168.1.1/path"
        result = LinkProcessor.toggle_www(url)
        self.assertEqual(result, "https://www.192.168.1.1/path")


if __name__ == '__main__':
    unittest.main()