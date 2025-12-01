"""Scraper to extract all versions, dates, and URLs from a webpage."""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd
import datetime
import time
import os
import re

class VersionOnlyScraper:
    """Extracts all version info, date, and associated URL from a webpage."""
    def __init__(self, driver_path="C:\\Users\\ASUS\\OneDrive\\Documents\\apexa\\week3\\News.html\\chromedriver.exe", headless=True):
        self.driver_path = driver_path
        self.headless = headless
        self.driver = self._setup_driver()
        self.output_folder = "output"
        os.makedirs(self.output_folder, exist_ok=True)
        self.versions_data = []

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
        print(f"Opened {url}")

    def expand_all_sections(self):
        """Expand all collapsible sections."""
        expandables = self.driver.find_elements(By.XPATH, "//details | //summary | //button")
        for exp in expandables:
            try:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", exp)
                self.driver.execute_script("arguments[0].click();", exp)
                time.sleep(0.3)
            except Exception:
                continue
        time.sleep(1)
        print(" Expanded all collapsible sections")

    def extract_versions(self):
        """Extract versions, dates, and URLs."""
        elements = self.driver.find_elements(By.XPATH, "//a | //p | //li | //div")
        for el in elements:
            text = el.text.strip()
            href = el.get_attribute("href") or ""

            if not text:
                continue

            # --- Extract version patterns (v1.2.3 or 1.2.3)
            version_match = re.search(r'\bv?(\d+\.\d+(\.\d+)*)\b', text, re.IGNORECASE)
            # --- Extract possible dates
            date_match = re.search(
                r'(\b\d{4}-\d{2}-\d{2}\b|\b[A-Za-z]{3,9}\s\d{1,2},\s?\d{4}\b|\b\d{1,2}\s[A-Za-z]{3,9}\s\d{4}\b)',
                text
            )

            if version_match:
                version = version_match.group(0)
                if not version.lower().startswith("v"):
                    version = f"v{version}"

                formatted_date = self.format_date(date_match.group(0)) if date_match else ""

                # Use href if it’s a proper URL
                url = href if href.startswith("http") else ""

                self.versions_data.append({
                    "Version": version,
                    "Date": formatted_date,
                    "URL": url
                })

    def format_date(self, date_str):
        """Normalize dates to YYYY-MM-DD format."""
        for fmt in ("%Y-%m-%d", "%B %d, %Y", "%d %B %Y", "%b %d, %Y", "%d %b %Y"):
            try:
                return datetime.datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
            except ValueError:
                continue
        return date_str  # return as-is if parsing fails

    def save_to_csv(self, filename="versions_only.csv"):
        """Save only version, date, and URL to CSV."""
        if not self.versions_data:
            print("⚠ No version data found.")
            return

        df = pd.DataFrame(self.versions_data).drop_duplicates(subset=["Version", "URL"])
        csv_path = os.path.join(self.output_folder, filename)
        df.to_csv(csv_path, index=False)
        print(f"Extracted {len(df)} entries saved to '{csv_path}'")

    def close_driver(self):
        self.driver.quit()
        print("Browser closed.")


# === Usage Example ===
if __name__ == "__main__":
    url = "https://www.dbf2002.com/news.html"  # Replace with target webpage
    scraper = VersionOnlyScraper(headless=True)
    scraper.open_website(url)
    scraper.expand_all_sections()
    scraper.extract_versions()
    scraper.save_to_csv()
    scraper.close_driver()
