# Browser-Use: AI Startup Website Analyzer

A Python-based web scraping and AI analysis tool that automatically analyzes websites to determine if they represent AI startups. The project combines web scraping, content extraction, and AI-powered text analysis to classify companies based on their website content.

## Features

- **Web Content Fetching**: Robust URL processing and HTML content retrieval
- **AI-Powered Analysis**: Uses OpenAI models to analyze website content
- **Batch Processing**: Analyze multiple URLs from CSV files
- **Error Handling**: Automatic retry with www prefix toggling for failed requests
- **Cost Tracking**: Monitor AI model usage costs and token consumption

## Project Structure

```
browser-use/
├── classes/
│   ├── models/
│   │   ├── models.py              # OpenAI API integration
│   │   └── model_pricing.py       # Cost calculation utilities
│   ├── processors/
│   │   ├── link_processor.py      # URL cleaning and validation
│   │   ├── soup_parser.py         # HTML parsing with BeautifulSoup
│   │   └── text_processor.py      # Text extraction and processing
│   ├── services/
│   │   └── website_ai_analyzer.py # Main analysis orchestration
│   └── web/
│       └── web_fetch.py           # HTTP request handling
├── tests/
│   └── test_linkprocessor.py      # Unit tests for URL processing
├── main.py                        # Entry point
├── requirements.txt               # Python dependencies
└── pytest.ini                    # Test configuration
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd browser-use
```

2. Create a virtual environment:
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory:
```env
WORK_OPENAI_API_KEY=your_openai_api_key_here
```

## Usage

### Basic Usage

Analyze a single URL:

```python
from classes.services.website_ai_analyzer import WebsiteAIAnalyzer

analyzer = WebsiteAIAnalyzer()
result = analyzer.analyze_url("https://example.com", "gpt-4.1-mini")
print(f"Is AI Startup: {result.extracted_answer}")
```

### Batch Analysis

Analyze multiple URLs from a CSV file:

```python
analyzer = WebsiteAIAnalyzer()
analyzer.analyze_urls(
    input_csv="startups.csv",
    output_csv="output.csv", 
    start_index=0,
    stop_index=10,
    model_name="gpt-4.1-mini"
)
```

### Input CSV Format

Your input CSV should have columns:
- `Startup name`: Company name
- `Website`: URL to analyze

Example:
```csv
Startup name,Website
Example Corp,https://example.com
AI Company,www.aicompany.com
```

## Core Components

### [`WebsiteAIAnalyzer`](classes/services/website_ai_analyzer.py)

The main orchestration class that coordinates:
- URL cleaning via [`LinkProcessor`](classes/processors/link_processor.py)
- Content fetching via [`WebFetch`](classes/web/web_fetch.py)
- HTML parsing via [`SoupParser`](classes/processors/soup_parser.py)
- AI analysis via [`Models`](classes/models/models.py)
- Answer extraction via [`TextProcessor`](classes/processors/text_processor.py)

### [`LinkProcessor`](classes/processors/link_processor.py)

Handles URL normalization:
- Ensures HTTPS protocol
- Removes query parameters and fragments
- Validates URL format
- Toggles www prefix for retry attempts

### [`WebFetch`](classes/web/web_fetch.py)

Manages HTTP requests:
- Custom headers and timeout handling
- Error handling for failed requests
- Returns structured response data

### [`Models`](classes/models/models.py)

OpenAI API integration:
- Chat completions API calls
- Token usage tracking
- Cost calculation via [`ModelPricing`](classes/models/model_pricing.py)

## Testing

Run the test suite:

```bash
pytest
```

Run specific tests:
```bash
pytest tests/test_linkprocessor.py -v
```

## Supported Models

Currently supports OpenAI models with pricing:
- `gpt-4.1-mini`: $0.40/$1.60 per 1M input/output tokens

Additional models can be added to [`ModelPricing`](classes/models/model_pricing.py).

## Output Format

The analysis generates CSV output with columns:
- Name
- Original URL
- Cleaned URL
- Status Code
- Page Load Success
- Model Response
- Extracted Answer (Yes/No/Unknown)
- Input Tokens
- Output Tokens
- Total Cost

## Error Handling

The system includes robust error handling:
- Automatic retry with www prefix toggling
- Graceful handling of network failures
- Content length limiting to prevent token overflow
- Comprehensive logging

## Dependencies

- `requests`: HTTP requests
- `beautifulsoup4`: HTML parsing
- `tiktoken`: Token counting
- `openpyxl`: Excel file support
- `openai`: OpenAI API client
- `pydantic`: Data validation
- `pandas`: Data manipulation

<!-- ## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request -->
