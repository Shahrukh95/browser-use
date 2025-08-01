from classes import LinkProcessor, SoupParser, WebFetch, Models
from classes.services.website_ai_analyzer import WebsiteAIAnalyzer
import pandas as pd
import logging

logging.basicConfig(
    filename='startups.log',
    filemode='w',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    analyzer = WebsiteAIAnalyzer()

    # Analyze a sample URL
    url = "https://asdasdasd123123asd1111.com"
    result = analyzer.analyze_url(url=url, model_name="gpt-4.1-mini")

    logging.info(f"Analysis Result: {result.model_dump()}")


if __name__ == "__main__":
    main()






# Example usage of WebDriver and LinkProcessor
# url = "https://192.168.1.1/path"
# # driver = WebDriver()
# link_processor = LinkProcessor()

# cleaned_url = link_processor.clean_url(url)
# print(f"Cleaned URL: {cleaned_url}")
# toggled_url = link_processor.toggle_www(cleaned_url)
# print(f"Toggled URL: {toggled_url}")

# input("Press Enter to close the browser...")
# # driver.quit()


# Example usage of WebDriver with a DataFrame
# driver = WebDriver()
# link_processor = LinkProcessor()

# df_startups = pd.read_csv("startups.csv")
# for index, row in df_startups.head(1).iterrows():
#     url = row['Website']
#     cleaned_url = link_processor.clean_url(url)
#     print(f"Cleaned URL: {cleaned_url}")

#     try:
#         driver.get(cleaned_url)
#     except Exception as e:
#         print(f"Error: Failed to navigate to {cleaned_url}")
#         continue

#     # driver.get(cleaned_url)
#     # input("Press Enter to close the browser...")
# driver.quit()