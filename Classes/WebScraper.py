from Classes.LinkProcessor import LinkProcessor
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, WebDriverException
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunparse, urljoin
import time
import re
import tiktoken
import re

class WebScraper(LinkProcessor):
    def __init__(self):
        self.__driver = super().__init__()
        self.__total_token_cost = 0
        self.__redirected_url = ""

    def set_token_cost(self, input_tokens, output_tokens, model_name):
        if model_name == "chatgpt-4o-latest":
            input_cost = (input_tokens / 1000) * 0.005
            output_cost = (output_tokens / 1000) * 0.015
            self.__total_token_cost += input_cost + output_cost
        elif model_name == "gpt-4o-mini":
            input_cost = (input_tokens / 1000) * 0.00015
            output_cost = (output_tokens / 1000) * 0.0006
            self.__total_token_cost += input_cost + output_cost
        elif model_name == "o3-mini":
            input_cost = (input_tokens / 1000) * 0.0011
            output_cost = (output_tokens / 1000) * 0.0044
            self.__total_token_cost += input_cost + output_cost
        elif model_name == "gpt-4o":
            input_cost = (input_tokens / 1000) * 0.0025
            output_cost = (output_tokens / 1000) * 0.01
            self.__total_token_cost += input_cost + output_cost
        elif model_name == "claude-3-7-sonnet-20250219" or model_name == "claude-sonnet-4-20250514":
            input_cost = (input_tokens / 1000) * 0.003
            output_cost = (output_tokens / 1000) * 0.015
            self.__total_token_cost += input_cost + output_cost
        elif model_name == "gpt-4o-search-preview":
            input_cost = (input_tokens / 1000) * 0.0025
            output_cost = (output_tokens / 1000) * 0.01
            self.__total_token_cost += input_cost + output_cost
        elif model_name == "deepseek-reasoner":
            input_cost = (input_tokens / 1000) * 0.00055
            output_cost = (output_tokens / 1000) * 0.00219
            self.__total_token_cost += input_cost + output_cost
        elif model_name == "gemini-1.5-pro":
            # for input and output tokens <= 128k tokens
            input_cost = (input_tokens / 1000) * 0.00125
            output_cost = (output_tokens / 1000) * 0.005
            self.__total_token_cost += input_cost + output_cost
        elif model_name == "gemini-2.0-flash-thinking-exp-01-21":
            # This cost is taken from the Gemini 2.0 Flash model
            input_cost = (input_tokens / 1000) * 0.0001
            output_cost = (output_tokens / 1000) * 0.0004
            self.__total_token_cost += input_cost + output_cost
        elif model_name == "mistral-large-latest":
            input_cost = (input_tokens / 1000) * 0.002
            output_cost = (output_tokens / 1000) * 0.006
            self.__total_token_cost += input_cost + output_cost
        else:
            raise ValueError("Model name not recognized. Token cost not calculated.")

    # --- Token methods ---
    def get_token_cost(self):
        return self.__total_token_cost

    def reset_token_cost(self):
        self.__total_token_cost = 0

    # --- URL methods ---
    def get_url(self):
        return self.__url
    
    def set_url(self, url):
        self.__url = self.clean_url(url)
        # print(f"Original URL: {url}. Cleaned URL: {self.__url}")

    # --- Redirection methods ---
    def set_redirect_url(self, redirected_url):
        self.__redirected_url = redirected_url

    def get_redirected_url(self):
        return self.__redirected_url
    
    def reset_redirect_url(self):
        self.__redirected_url = ""

    def open_url(self):
        try:
            self.__driver.set_page_load_timeout(15)  # Set the timeout to 15 seconds
            self.__driver.get(self.__url)

            if self.__driver.current_url != self.__url:
                print(f"Redirected to {self.__driver.current_url}")
                self.set_redirect_url(self.__driver.current_url)
                self.set_url(self.__driver.current_url)
            return 200
        except TimeoutException:
            print(f"Page load timeout: {self.__url}. Stopping page load.")
            self.__driver.execute_script("window.stop();")  # Stop the loading
        except Exception as e:
            print(f"Error opening URL {self.__url}")
            return 0 # General Error

    def quit_driver(self):
        self.__driver.quit()

    def load_page(self):
        status = self.open_url()
        # If there was a DNS failure, toggle the www. part and try again
        if status == 0:  
            current_url = self.get_url()
            new_url = self.toggle_www(current_url)

            if new_url:
                print(f"Retrying with {new_url}")
                self.set_url(new_url)
                status = self.open_url()

                if status == 0:
                    print("Toggling www did not work.")
                    self.set_url(current_url)  # Reset to original URL
                else:
                    self.set_redirect_url(self.get_url())


        self.cookie_acceptor()
        self.page_scroller()
        self.set_html_innerHTML()

    def get_page_content(self, model_name):
        page_content = self.scrape_page_content(model_name)
        return page_content
    
    def get_page_links(self):
        page_links = self.scrape_page_links(self.__url)
        return page_links





    # Copied methods from LinkProcessor
    
    def find_elements_by_xpath(self, xpath):
        try:
            elements = self.__driver.find_elements(By.XPATH, xpath)
            return elements
        except NoSuchElementException:
            # print(f"Element with XPath {xpath} not found. Function: find_elements_by_xpath")
            return []
        except Exception as e:  
            # print(f"Unexpected error on XPath {xpath}. Reason: {e}. Function: find_elements_by_xpath")
            return []

    def page_scroller(self):
        start_time = time.time()

        while True:
            # Scroll by viewport height
            self.__driver.execute_script("window.scrollBy(0, window.innerHeight);")
            time.sleep(0.5)

            # Calculate how far we have scrolled and how much is remaining
            scrolled_height = self.__driver.execute_script("return Math.round(window.pageYOffset);")
            total_scrollable_height = self.__driver.execute_script("return Math.round(document.body.scrollHeight);")
            visible_height = self.__driver.execute_script("return Math.round(window.innerHeight);")

            elapsed_time = time.time() - start_time

            # Break conditions: 1) We have reached the end of the page 2) Elapsed time is greater than the maximum allowed time
            if (scrolled_height + visible_height >= total_scrollable_height - 5) or (elapsed_time > LinkProcessor.MAX_TIME_SECONDS):
                break
    
    def cookie_acceptor(self):
        cookie_button_labels = ["Accept", "Accept All", "Allow All", "Agree", "Got it", "Continue", "OK", "I Accept", "I Agree", "Allow", "Accept Cookies", "Yes, I Agree", "Akzeptieren", "Einverstanden", "Zustimmen", "Fortfahren", "Ablehnen", "Alle auswählen", "auswählen", "Alle akzeptieren", "Alles akzeptieren", "Alle ablehnen", "Zustimmen und weiter", "Alle zulassen"]

        potential_cookie_elems = self.find_elements_by_xpath("//button") + self.find_elements_by_xpath("//a")
        for element in potential_cookie_elems:
            try:
                potential_cookie_word = element.text.strip()
                # Compare only in lowercase
                if potential_cookie_word.lower() in [x.lower() for x in cookie_button_labels]:
                    element.click()
                    # print(f"Cookie acceptor found and clicked: {potential_cookie_word}")
                    time.sleep(1)
                    return True
            except StaleElementReferenceException:
                # print("StaleElementReferenceException encountered. Retrying...")
                continue  # Retry by checking the next element
            except NoSuchElementException:
                # print("NoSuchElementException: Element may have been removed.")
                continue
            except Exception as e:
                # print(f"An unexpected exception occurred: {e}")
                continue
        
        # print("Cookie acceptor not found")
        return False

    def count_tokens(self, text, model_name):
        encoding = tiktoken.encoding_for_model(model_name)
        tokens = encoding.encode(text)
        return len(tokens)
    
    def clean_text(self, text):
        # Clean the text: Remove extra spaces and newlines
        return re.sub(r'\s+', ' ', text).strip()

    # Retreive the innerHTML of the html tag, do not clean it
    def set_html_innerHTML(self):
        body_element = self.__driver.find_element(By.TAG_NAME, "html")
        self.__body_html = body_element.get_attribute("innerHTML")

    # Parse the HTML content into text
    def get_body_text(self):
        soup = BeautifulSoup(self.__body_html, "html.parser")
        all_text = soup.get_text(separator=" ")
        
        # Combine <iframe> and <frame> handling
        iframe_text = ""
        frames = self.__driver.find_elements(By.TAG_NAME, "iframe") + self.__driver.find_elements(By.TAG_NAME, "frame")
        for frame in frames:
            try:
                self.__driver.switch_to.frame(frame)  # Switch to the frame/iframe
                frame_soup = BeautifulSoup(self.__driver.page_source, "html.parser")
                iframe_text += frame_soup.get_text(separator=" ")
                self.__driver.switch_to.default_content()  # Switch back to the main content
            except WebDriverException:
                # Skip if the frame/iframe is restricted or inaccessible
                continue
        
        # Combine the main content and iframe/frame content
        all_text += "\n\n" + iframe_text
        return self.clean_text(all_text)

    def scrape_page_content(self, model_name):
        # print(self.__body_html)

        all_text = self.get_body_text()

        body_length = len(all_text)
        # print(f"Page character length: {body_length}")
        tokens = self.count_tokens(all_text, model_name)
            
        while tokens > 8000:
            print(f"Token count: {tokens}. Text too long. Truncating 1000 letters.")
            all_text = all_text[:-1000]
            tokens = self.count_tokens(all_text, model_name)
        
        # print(f"Token count in raw page: {tokens}")

        # Remove illegal characters that would not save in Excel
        all_text = escape(all_text)

        return all_text
    
    def scrape_page_links(self, source_url):
        soup = BeautifulSoup(self.__body_html, "html.parser")
        links = soup.find_all("a", href=True)

        same_domain_links = []
        for link in links:
            url_found = self.clean_url(urljoin(source_url, link['href']))  # Resolve relative URL and clean
            parsed_link = urlparse(url_found)
            # print(f"Found URL: {url_found}")

            # Check if the found url is from the main domain, not already in the list and not the source URL (i.e. homepage)
            if urlparse(source_url).hostname == parsed_link.hostname and url_found not in same_domain_links and url_found != source_url:
                same_domain_links.append(url_found)
            
            if len(same_domain_links) > 80:
                break

        # print(f"Links found: {same_domain_links}")
        return same_domain_links
