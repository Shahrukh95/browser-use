from Classes import WebDriver, LinkProcessor

def main():
    url = "https://192.168.1.1/path"
    # driver = WebDriver()
    link_processor = LinkProcessor()

    cleaned_url = link_processor.clean_url(url)
    print(f"Cleaned URL: {cleaned_url}")
    toggled_url = link_processor.toggle_www(cleaned_url)
    print(f"Toggled URL: {toggled_url}")

    input("Press Enter to close the browser...")
    # driver.quit()


if __name__ == "__main__":
    main()