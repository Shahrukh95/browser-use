from Classes import WebDriver

def main():
    driver_obj = WebDriver()
    driver = driver_obj.get_driver()
    driver.get("https://www.example.com")

    input("Press Enter to close the browser...")
    driver.quit()


if __name__ == "__main__":
    main()