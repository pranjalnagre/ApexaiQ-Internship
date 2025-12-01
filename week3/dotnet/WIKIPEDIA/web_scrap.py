"""File for scraping all tables from a webpage and saving as a single CSV."""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import datetime
import time
import os

class WindowsServerScraper:
    """Scraper class to extract tables from a webpage and save as a single CSV."""
    def __init__(self, driver_path="C:\\Users\\ASUS\\OneDrive\\Documents\\apexa\\week3\\WIKIPEDIA\\chromedriver.exe", headless=True):
        self.driver_path = driver_path
        self.headless = headless
        self.driver = self._setup_driver()
        self.wait = WebDriverWait(self.driver, 10)
        self.tables_data = []
        self.output_folder = "output"
        os.makedirs(self.output_folder, exist_ok=True)

    def _setup_driver(self):
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--log-level=3")
        service = Service(self.driver_path)
        return webdriver.Chrome(service=service, options=chrome_options)

    def open_website(self, url):
        """Opens the given website URL."""
        self.driver.get(url)
        time.sleep(2)

    def expand_sections(self):
        """Expands collapsible sections if any (modify XPath if needed)."""
        sections = self.driver.find_elements(By.XPATH, "//*[@id='Release_table']")
        for section in sections:
            try:
                self.driver.execute_script("arguments[0].scrollIntoView();", section)
                time.sleep(1)
                self.driver.execute_script("arguments[0].click();", section)
                time.sleep(2)
            except Exception as e:
                print(f"Could not expand section: {e}")

    def format_date(self, text):
        """Formats date strings to YYYY-MM-DD if possible."""
        for fmt in ("%B %d, %Y", "%d %B %Y", "%b %d, %Y", "%d %b %Y"):
            try:
                parsed_date = datetime.datetime.strptime(text, fmt)
                return parsed_date.strftime("%Y-%m-%d")
            except ValueError:
                continue
        return text

    def extract_tables(self):
        """Extracts all tables on the page."""
        tables = self.driver.find_elements(By.XPATH, "//table")
        for idx, table in enumerate(tables):
            try:
                rows = table.find_elements(By.XPATH, ".//tr")
                table_data = []
                for row_idx, row in enumerate(rows):
                    cols = row.find_elements(By.XPATH, ".//th" if row_idx == 0 else ".//td")
                    formatted_cols = [self.format_date(col.text.strip()) for col in cols]
                    if formatted_cols:
                        table_data.append(formatted_cols)
                if table_data:
                    df = pd.DataFrame(table_data[1:], columns=self.make_columns_unique(table_data[0]))
                    self.tables_data.append(df)
            except Exception as e:
                print(f"⚠ Error extracting table {idx+1}: {e}")

    def make_columns_unique(self, columns):
        """Ensure column names are unique when merging multiple tables."""
        seen = {}
        new_columns = []
        for col in columns:
            if col not in seen:
                seen[col] = 0
                new_columns.append(col)
            else:
                seen[col] += 1
                new_columns.append(f"{col}_{seen[col]}")
        return new_columns

    def save_to_csv(self, filename="all_tables_combined.csv"):
        """Merge all tables and save to a single CSV."""
        if not self.tables_data:
            print("No tables found to save.")
            return
        combined_df = pd.concat(self.tables_data, ignore_index=True, sort=False)
        csv_path = os.path.join(self.output_folder, filename)
        combined_df.to_csv(csv_path, index=False)
        print(f"All tables combined and saved to '{csv_path}'")

    def close_driver(self):
        """Closes the Selenium WebDriver."""
        self.driver.quit()



if __name__ == "__main__":
    scraper = WindowsServerScraper()
    scraper.open_website("https://en.wikipedia.org/wiki/Java_version_history")
    scraper.expand_sections()
    scraper.extract_tables()
    scraper.save_to_csv()
    scraper.close_driver()
