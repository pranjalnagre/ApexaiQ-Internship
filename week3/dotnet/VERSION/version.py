"""Enhanced scraper for extracting all visible data (tables, lists, and text) from any VersionsOf.net page."""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import json
import datetime
import time
import os

class WindowsServerScraper:
    """Comprehensive scraper to extract all visible structured data from VersionsOf.net or Microsoft Wiki pages."""
    def __init__(self, driver_path="C:\\Users\\ASUS\\OneDrive\\Documents\\apexa\\week3\\VERSION\\chromedriver.exe", headless=True):
        self.driver_path = driver_path
        self.headless = headless
        self.driver = self._setup_driver()
        self.wait = WebDriverWait(self.driver, 10)
        self.output_folder = "output"
        os.makedirs(self.output_folder, exist_ok=True)
        self.tables_data = {}
        self.all_text_data = []

    def _setup_driver(self):
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--log-level=3")
        service = Service(self.driver_path)
        return webdriver.Chrome(service=service, options=chrome_options)

    def open_website(self, url):
        self.driver.get(url)
        time.sleep(3)

    def expand_all_sections(self):
        """Expands any collapsible or hidden sections dynamically."""
        expanders = self.driver.find_elements(By.XPATH, "//details | //button | //summary")
        for exp in expanders:
            try:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", exp)
                self.driver.execute_script("arguments[0].click();", exp)
                time.sleep(0.5)
            except Exception:
                pass
        time.sleep(2)

    def format_date(self, text):
        try:
            parsed_date = datetime.datetime.strptime(text, "%B %d, %Y")
            return parsed_date.strftime("%Y%m%d")
        except ValueError:
            return text

    def extract_tables(self):
        """Extract all HTML tables and convert them to DataFrames."""
        tables = self.driver.find_elements(By.XPATH, "//table")
        for idx, table in enumerate(tables):
            try:
                rows = table.find_elements(By.XPATH, ".//tr")
                data = []
                for i, row in enumerate(rows):
                    cells = row.find_elements(By.XPATH, ".//th|.//td")
                    data.append([cell.text.strip() for cell in cells])
                if len(data) > 1:
                    headers = data[0]
                    df = pd.DataFrame(data[1:], columns=headers)
                    self.tables_data[f"table_{idx+1}"] = df
            except Exception as e:
                print(f"⚠ Error extracting table {idx+1}: {e}")

    def extract_text_blocks(self):
        """Extract all headings, paragraphs, and lists for contextual data."""
        content_elements = self.driver.find_elements(
            By.XPATH, "//h1|//h2|//h3|//h4|//h5|//h6|//p|//li|//pre|//code"
        )
        for el in content_elements:
            text = el.text.strip()
            tag = el.tag_name
            if text:
                self.all_text_data.append({"tag": tag, "text": text})

    def save_data(self):
        """Save all data (tables + text) into CSV and JSON."""
        # Save tables
        if self.tables_data:
            combined_csv_path = os.path.join(self.output_folder, "all_tables.csv")
            combined_dfs = []
            for name, df in self.tables_data.items():
                df["Source_Table"] = name
                combined_dfs.append(df)
            pd.concat(combined_dfs, ignore_index=True).to_csv(combined_csv_path, index=False)
            print(f"Tables saved to '{combined_csv_path}'")
        else:
            print("⚠ No tables found.")

        # Save text content
        if self.all_text_data:
            json_path = os.path.join(self.output_folder, "all_text_data.json")
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(self.all_text_data, f, ensure_ascii=False, indent=2)
            print(f"Text content saved to '{json_path}'")
        else:
            print("⚠ No text data found.")

    def close_driver(self):
        self.driver.quit()


# === Usage Example ===
if __name__ == "__main__":
    url = "https://versionsof.net/core/8.0/8.0.0/"
    scraper = WindowsServerScraper(headless=True)
    scraper.open_website(url)
    scraper.expand_all_sections()
    scraper.extract_tables()
    scraper.extract_text_blocks()
    scraper.save_data()
    scraper.close_driver()
