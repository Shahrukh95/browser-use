from classes import LinkProcessor, SoupParser, WebFetch
import pandas as pd
import logging

logging.basicConfig(
    filename='startups.log',
    filemode='w',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():

    link_processor = LinkProcessor()
    url = "example.com/search?q=python+programming"
    cleaned_url = link_processor.clean_url(url)

    web_data = WebFetch.fetch_url(cleaned_url)
    if web_data:
        logging.info(f"Final URL: {web_data['final_url']}")
        logging.info(f"Toggled URL: {link_processor.toggle_www(web_data['final_url'])}")
        logging.info(f"Status Code: {web_data['status_code']}")
        # logging.info(f"Content Preview: {web_data['html_content'][:100]}...")

        # Example usage of SoupParser
        content = SoupParser.get_content(web_data['html_content'])
        title = SoupParser.get_title(web_data['html_content'])

        logging.info(f"Page Title: {title}")
        logging.info(f"Page Content: {content[:100]}...")
        logging.info(f"Content length: {len(content)}")


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