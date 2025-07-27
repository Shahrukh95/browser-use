from Classes import WebDriver, LinkProcessor
import pandas as pd

def main():
    # url = "https://192.168.1.1/path"
    # # driver = WebDriver()
    # link_processor = LinkProcessor()

    # cleaned_url = link_processor.clean_url(url)
    # print(f"Cleaned URL: {cleaned_url}")
    # toggled_url = link_processor.toggle_www(cleaned_url)
    # print(f"Toggled URL: {toggled_url}")

    # input("Press Enter to close the browser...")
    # # driver.quit()

    driver = WebDriver()
    link_processor = LinkProcessor()

    df_startups = pd.read_csv("startups.csv")
    for index, row in df_startups.head(1).iterrows():
        url = row['Website']
        cleaned_url = link_processor.clean_url(url)
        print(f"Cleaned URL: {cleaned_url}")

        try:
            driver.get(cleaned_url)
        except Exception as e:
            print(f"Error: Failed to navigate to {cleaned_url}")
            continue

        # driver.get(cleaned_url)
        # input("Press Enter to close the browser...")
    driver.quit()
        
            
    


if __name__ == "__main__":
    main()