from selenium import webdriver
import tempfile

class WebDriver():
    def __init__(self):

        unique_dir = tempfile.mkdtemp()
        # chrome_profile_path = r"C:\Users\ShahrukhAzharAhsan\AppData\Local\Google\Chrome\User Data"

        self.__chrome_options = webdriver.ChromeOptions()
        # self.__chrome_options.add_argument("--headless=new")
        self.__chrome_options.add_argument(f"user-data-dir={unique_dir}")
        # self.__chrome_options.add_argument("profile-directory=Default")
        
        # Required for running in docker
        self.__chrome_options.add_argument("--no-sandbox")
        self.__chrome_options.add_argument("--disable-dev-shm-usage")  # Prevent shared memory issues. Also required in docker because shared memory is 64mb only in docker.

        self.__chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        self.__chrome_options.add_argument('--window-size=1920,1080')
        # self.__chrome_options.add_argument("--incognito")
        self.__chrome_options.add_argument("--log-level=3")

        # Disable GPU
        # self.__chrome_options.add_argument("--disable-gpu")  # Disables GPU acceleration
        # self.__chrome_options.add_argument("--disable-software-rasterizer")  # Further prevents GPU issues
        self.__chrome_options.add_argument("--enable-webgl")

        self.__driver = None


    def _ensure_driver(self):
        """Lazy initialization of the driver"""
        if self.__driver is None:
            self.__driver = webdriver.Chrome(options=self.__chrome_options)

    def get_driver(self):
        """Get the underlying driver"""
        self._ensure_driver()
        return self.__driver
    
    def get(self, url):
        """Navigate to URL"""
        self._ensure_driver()
        print(f"Navigating to {url}")
        return self.__driver.get(url)
    
    def quit(self):
        """Close the browser"""
        if self.__driver:
            print("Closing the browser...")
            self.__driver.quit()
            self.__driver = None
