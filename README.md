# ArabamScraper

ArabamScraper is a web scraping tool designed to collect second-hand vehicle listings from Arabam.com. The script extracts essential vehicle details such as brand, model, year, price, mileage, listing date, and location, saving the data into a structured CSV file. This project is currently intended for generating a small dataset, with future updates planned for improvements and expanded functionality.

## Features
- Uses Selenium and BeautifulSoup for efficient web scraping.
- Implements human-like browsing behavior to avoid detection.
- Saves extracted data into a CSV file for easy analysis.
- Configurable maximum page limit to control the scraping process.

## Requirements
- Python 3.x
- Google Chrome & ChromeDriver
- Required Python libraries: `beautifulsoup4`, `selenium`, `csv`

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/ArabamScraper.git
   cd ArabamScraper
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Ensure ChromeDriver is installed and matches your Chrome version.

## Usage
Run the script with:
```sh
python arabam_scraper.py --category otomobil --min_price 50000 --max_price 200000 --max-pages 5 --output car_listings.csv
```
The scraped data will be saved as a CSV file in the project directory.

## Future Updates
- Enhancements for larger dataset collection.
- Improved error handling and performance optimizations.
- Additional filtering and data extraction features.

## License
This project is licensed under the MIT License.

