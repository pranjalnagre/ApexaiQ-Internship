""" File for scraping Windows Server release tables from the Microsoft Wiki page."""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import datetime
import time
import os

class WindowsServerScraper:
    """Scraper class to extract Windows Server tables from the Microsoft Wiki page."""
    def __init__(self, driver_path="C:\\Users\\ASUS\\OneDrive\\Documents\\apexa\\week3\\oracle\\chromedriver.exe", headless=True):
        self.driver_path = driver_path
        self.headless = headless
        self.driver = self._setup_driver()
        self.wait = WebDriverWait(self.driver, 10)
        self.tables_data = {}
        self.output_folder = "output"
        os.makedirs(self.output_folder, exist_ok=True)

    def _setup_driver(self):
        """Initialize and configure the Selenium WebDriver."""
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
        """Expands all collapsible sections on the webpage."""
        sections = self.driver.find_elements(By.XPATH, "//span[contains(@class, 'mw-headline')]")
        for section in sections:
            try:
                self.driver.execute_script("arguments[0].scrollIntoView();", section)
                time.sleep(1)
                self.driver.execute_script("arguments[0].click();", section)
                time.sleep(3)
            except Exception as e:
                print(f" Could not expand section: {e}")
        time.sleep(3)

    def format_date(self, text):
        """Formats date strings to yyyymmdd format if possible."""
        try:
            parsed_date = datetime.datetime.strptime(text, "%B %d, %Y")
            return parsed_date.strftime("%Y%m%d")
        except ValueError:
            return text  

    def extract_tables(self):
        """Extracts tables from the webpage and stores them in a structured dictionary."""
        tables = self.driver.find_elements(By.XPATH, "//table")

        for idx, table in enumerate(tables):
            try:
                rows = table.find_elements(By.XPATH, ".//tr")
                table_data = []
                header_length = 0

                for row_idx, row in enumerate(rows):
                    cols = row.find_elements(By.XPATH, ".//th" if row_idx == 0 else ".//td")
                    formatted_cols = [self.format_date(col.text.strip()) for col in cols]

                    # Capture header length on first row
                    if row_idx == 0:
                        header_length = len(formatted_cols)

                    # For data rows, pad or truncate to match header length
                    else:
                        if len(formatted_cols) < header_length:
                            formatted_cols += [''] * (header_length - len(formatted_cols))
                        elif len(formatted_cols) > header_length:
                            formatted_cols = formatted_cols[:header_length]

                    if formatted_cols:
                        table_data.append(formatted_cols)

                if table_data:
                    column_titles = tuple(table_data[0])  # Use header row as key
                    df = pd.DataFrame(table_data[1:], columns=table_data[0])  # DataFrame with headers

                    if column_titles in self.tables_data:
                        self.tables_data[column_titles].append(df)
                    else:
                        self.tables_data[column_titles] = [df]

            except Exception as e:
                print(f"⚠ Error extracting table {idx+1}: {e}")

    def make_columns_unique(self, columns):
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

    def save_to_csv(self, filename="windows_server_data.csv"):
        all_dfs = []

        for dfs in self.tables_data.values():
            for df in dfs:
                df.columns = self.make_columns_unique(df.columns)  # Use self. here
                all_dfs.append(df)

        if all_dfs:
            final_df = pd.concat(all_dfs, ignore_index=True, sort=False)
            csv_path = os.path.join(self.output_folder, filename)
            final_df.to_csv(csv_path, index=False)
            print(f"All data combined and saved to '{csv_path}'.")
        else:
            print("No tables found to save.")


    def close_driver(self):
        """Closes the Selenium WebDriver."""
        self.driver.quit()

# Usage
scraper = WindowsServerScraper()
scraper.open_website("https://en.wikipedia.org/wiki/Oracle_Linux")
scraper.expand_sections()
scraper.extract_tables()
scraper.save_to_csv()
scraper.close_driver()