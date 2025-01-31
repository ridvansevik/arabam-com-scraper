from bs4 import BeautifulSoup
import csv
import time
import random
from selenium import webdriver
import argparse

class ArabamScraper:
    def __init__(self, category, min_price, max_price, output_file_name, max_pages):
        """Initializes the scraper with necessary parameters.

        Args:
            category (str): The category to scrape (e.g., 'otomobil', 'motosiklet').
            min_price (int): Minimum price filter.
            max_price (int): Maximum price filter.
            output_file_name (str): Name of the output CSV file.
            max_pages (int): Maximum number of pages to scrape.
        """

        self.category = category
        self.min_price = min_price
        self.max_price = max_price
        self.output_file_name = output_file_name
        self.max_pages = max_pages
        self.base_url = self._build_url()
        self.driver = self._initialize_driver()
    
    def _initialize_driver(self):
        """Initializes the Selenium WebDriver with necessary options.
        
        Returns:
            webdriver.Chrome: A configured Selenium WebDriver instance.
        """
        try:
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")  # Run Chrome in headless mode.
            options.add_argument("--no-sandbox")  # Bypass OS security model.
            options.add_argument("--disable-dev-shm-usage")  # Overcome limited resources.
            options.add_argument("start-maximized")  # Start browser maximized.
            options.add_argument("disable-infobars")  # Prevent infobars from appearing.
            options.add_argument("--disable-blink-features=AutomationControlled")  # Avoid detection.
            options.add_argument('--ignore-certificate-errors')  # Ignore SSL certificate errors.
            options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36")
            
            driver = webdriver.Chrome(options=options)
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")  # Further anti-detection measures.
            return driver
        except Exception as e:
            print(f"[ERROR] Failed to initialize WebDriver: {e}")
            return None
    
    def _build_url(self, page=1):
        url = f"https://www.arabam.com/ikinci-el/{self.category}?currency=TL&minPrice={self.min_price}&maxPrice={self.max_price}&take=50&page={page}"
        print(f"You are taking {self.category}'s between {self.min_price} and {self.max_price} TL.")
        return url
    
    def _get_page_soup(self, url):
        """Fetches the page content and returns a BeautifulSoup object.
        
        Args:
            url (str): The URL of the page to fetch.
        
        Returns:
            BeautifulSoup: A parsed HTML document.
        """
        time.sleep(random.uniform(2, 5))  # Introduce a random delay to avoid detection.
        try:
            self.driver.get(url)
            page_source = self.driver.page_source
            return BeautifulSoup(page_source, 'html.parser')
        except Exception as e:
            print(f"[ERROR] Failed to fetch page: {e}")
            return None
    
    def _get_total_pages(self):
        """Determines the total number of pages available for scraping.
        
        Returns:
            int: The total number of pages to scrape.
        """
        soup = self._get_page_soup(self.base_url)
        if not soup:
            return 1
        
        pagination = soup.select(".pagination a")  # Locate pagination links.
        page_numbers = [int(a.get_text(strip=True)) for a in pagination if a.get_text(strip=True).isdigit()]
        return max(page_numbers) if page_numbers else 1
    
    def _save_to_csv(self, column_headers, row_datas):
        """Saves the scraped data into a CSV file.
        
        Args:
            column_headers (list): The header row for the CSV file.
            row_datas (list): The data rows to be written to the file.
        """
        try:
            with open(self.output_file_name, mode='w', newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file)
                writer.writerow(column_headers)
                for row in row_datas:
                    writer.writerow(row)
        except Exception as e:
            print(f"[ERROR] Failed to save CSV: {e}")
    
    def _extract_car_data(self, page_content):
        """Extracts car details from the page content.
        
        Args:
            page_content (BeautifulSoup): The parsed HTML content.
        
        Returns:
            tuple: Column names and extracted row data.
        """
        row_datas = []
        column_names = ["Brand", "Model", "Year", "Price", "Mileage", "Listing Date", "Location"]
        
        rows = page_content.select('tr.listing-list-item')  # Locate listing rows.
        for row in rows:
            try:
                year = row.find_all('td')[3].find('div', class_='fade-out-content-wrapper').find('a').text.strip()
                model_full = row.find('td', class_='listing-modelname pr').find('h3').text.strip()
                brand, model = model_full.split(' ', 1)  # Split brand and model.
                mileage = row.find_all('td')[4].find('div', class_='fade-out-content-wrapper').find('a').text.strip().replace(".", "")
                price_tag = row.find_all('td')[6].find('div', class_='fade-out-content-wrapper').find('a')
                price = price_tag.find('span', class_='db no-wrap listing-price').text.strip() if price_tag else 'N/A'

                listing_date = row.find('td', class_='listing-text tac').find('div', class_='fade-out-content-wrapper').find('a').text.strip()
                location = row.find_all('td')[8].find('div').find('div', class_='fade-out-content-wrapper').find('a').find_all('span')[0].text.strip()
                
                row_datas.append([brand, model, year, price, mileage, listing_date, location])
            except AttributeError:
                print("[WARNING] Missing data detected, skipping entry.")
                continue
        
        return column_names, row_datas

    def scrape(self):
        """Main method to scrape data from the website."""
        if not self.driver:
            return
        
        total_pages = min(self._get_total_pages(), self.max_pages)
        print(f"Total pages to scrape: {total_pages}")
        
        all_rows_data = []
        column_names = []
        
        for page_num in range(1, total_pages + 1):
            url = self._build_url(page_num)
            print(f"Processing: {url}")
            page_content = self._get_page_soup(url)
            if not page_content:
                continue
            column_names, rows_data = self._extract_car_data(page_content)
            all_rows_data.extend(rows_data)
            print(f"Page {page_num} - Listings extracted: {len(rows_data)}")
        
        if all_rows_data:
            self._save_to_csv(column_names, all_rows_data)
            print(f"Total {len(all_rows_data)} listings scraped and saved to CSV.")
        
        self.driver.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Arabam.com Scraper")
    parser.add_argument("--max-pages", type=int, default=2, help="Maximum number of pages to scrape")
    parser.add_argument("--category", type=str, default="otomobil", help="Choose Category ('otomobil', 'motosiklet')")
    parser.add_argument("--min_price", type=int, default=0, help="Min Price")
    parser.add_argument("--max_price", type=int, default=100000000, help="Max Price")
    parser.add_argument("--output", type=str, default="InformationsOutput.csv", help="Output CSV file name")

    args = parser.parse_args()

    scraper = ArabamScraper(
    category=args.category,
    min_price=args.min_price,
    max_price=args.max_price,
    output_file_name=args.output,
    max_pages=args.max_pages
)

    
    scraper.scrape()