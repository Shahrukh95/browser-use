import pytest
import sys
import os

# Add the parent directory to the path to import Classes
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from classes.processors.link_processor import LinkProcessor


@pytest.fixture
def processor():
    """Fixture that provides a LinkProcessor instance"""
    return LinkProcessor()
# Clean URL tests
def test_clean_url_with_https():
    """Test clean_url with https URL"""
    url = "https://example.com/path?query=123#fragment"
    result = LinkProcessor.clean_url(url)
    assert result == "https://example.com/path"

def test_clean_url_without_scheme():
    """Test clean_url without scheme - should add https"""
    url = "example.com/path?query=123"
    result = LinkProcessor.clean_url(url)
    assert result == "https://example.com/path"

def test_clean_url_with_http():
    """Test clean_url with http - should convert to https"""
    url = "http://example.com/path"
    result = LinkProcessor.clean_url(url)
    assert result == "https://example.com/path"

def test_clean_url_removes_query_and_fragment():
    """Test that query parameters and fragments are removed"""
    url = "https://example.com/path?query=123&other=456#section"
    result = LinkProcessor.clean_url(url)
    assert result == "https://example.com/path"

def test_clean_url_with_empty_string():
    """Test clean_url with empty string - should raise ValueError"""
    with pytest.raises(ValueError):
        LinkProcessor.clean_url("")

def test_clean_url_with_none():
    """Test clean_url with None - should raise ValueError"""
    with pytest.raises(ValueError):
        LinkProcessor.clean_url(None)

def test_clean_url_with_non_string():
    """Test clean_url with non-string input"""
    with pytest.raises(ValueError):
        LinkProcessor.clean_url(123)

def test_clean_url_with_invalid_url():
    """Test clean_url with invalid URL format"""
    with pytest.raises(ValueError):
        LinkProcessor.clean_url("not-a-valid-url")

def test_clean_url_with_ipv4_address():
    """Test clean_url with IPv4 address"""
    url = "192.168.1.1/path?query=123"
    result = LinkProcessor.clean_url(url)
    assert result == "https://192.168.1.1/path"

def test_clean_url_with_ipv4_and_port():
    """Test clean_url with IPv4 address and port"""
    url = "http://192.168.1.1:8080/api"
    result = LinkProcessor.clean_url(url)
    assert result == "https://192.168.1.1:8080/api"

def test_clean_url_with_subdomain():
    """Test clean_url with subdomain"""
    url = "api.example.com/v1/users"
    result = LinkProcessor.clean_url(url)
    assert result == "https://api.example.com/v1/users"

def test_clean_url_with_port():
    """Test clean_url with port number"""
    url = "https://example.com:8443/secure"
    result = LinkProcessor.clean_url(url)
    assert result == "https://example.com:8443/secure"

def test_clean_url_with_trailing_slash():
    """Test clean_url with trailing slash"""
    url = "https://example.com/"
    result = LinkProcessor.clean_url(url)
    assert result == "https://example.com/"

def test_clean_url_with_deep_path():
    """Test clean_url with deep path structure"""
    url = "example.com/api/v1/users/123/posts"
    result = LinkProcessor.clean_url(url)
    assert result == "https://example.com/api/v1/users/123/posts"

def test_clean_url_with_whitespace():
    """Test clean_url with leading/trailing whitespace"""
    url = "  https://example.com/path  "
    result = LinkProcessor.clean_url(url)
    assert result == "https://example.com/path"

def test_clean_url_root_domain_only():
    """Test clean_url with root domain only"""
    url = "example.com"
    result = LinkProcessor.clean_url(url)
    assert result == "https://example.com"

def test_clean_url_with_special_characters_in_path():
    """Test clean_url with special characters in path"""
    url = "example.com/path-with_special.chars/123"
    result = LinkProcessor.clean_url(url)
    assert result == "https://example.com/path-with_special.chars/123"



# Toggle www tests
def test_toggle_www_add_www():
    """Test adding www to URL without it"""
    url = "https://example.com/path"
    result = LinkProcessor.toggle_www(url)
    assert result == "https://www.example.com/path"

def test_toggle_www_remove_www():
    """Test removing www from URL with it"""
    url = "https://www.example.com/path"
    result = LinkProcessor.toggle_www(url)
    assert result == "https://example.com/path"

def test_toggle_www_with_subdomain():
    """Test toggle_www with existing subdomain"""
    url = "https://api.example.com/path"
    result = LinkProcessor.toggle_www(url)
    assert result == "https://www.api.example.com/path"

def test_toggle_www_with_ip_address():
    """Test toggle_www with IP address"""
    url = "192.168.1.1/path"
    result = LinkProcessor.toggle_www(url)
    assert result == "https://www.192.168.1.1/path"