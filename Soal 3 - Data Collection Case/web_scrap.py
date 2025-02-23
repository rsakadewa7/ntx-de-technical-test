from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import polars as pl
import json
import os

# Set up Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no UI)
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

service = Service("/path/to/chromedriver")  # Replace with correct path
driver = webdriver.Chrome(service=service, options=chrome_options)

max_pages = 5  # Adjust based on actual data availability
skipped_pages = []

def scrape_page(level, page):
    url = f"https://www.fortiguard.com/encyclopedia?type=ips&risk={level}&page={page}"
    driver.get(url)
    time.sleep(5)  # Wait for JavaScript to load

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    data = []
    for item in soup.find_all('div', class_='row py-2'):
        # Level 1
        level_1 = item.find('small')
        level_1_text = level_1.text.strip() if level_1 else "N/A"

        # Level 2
        level_2 = item.find('div', class_='col-lg')
        level_2_text = level_2.find('b').text.strip() if level_2 and level_2.find('b') else "N/A"

        # Level 3
        level_3 = item.find('small')
        level_3_text = level_3.text.strip() if level_3 else "N/A"

        # Level 4 (Count dark circles)
        level_4 = item.find('div', class_='col-lg-auto')
        dark_circles = level_4.find_all('img', alt='black-background-circle-icon') if level_4 else []
        risk_score = len(dark_circles)

        # Level 5 (Date)
        level_5 = item.find('div', class_='col-lg-auto')
        level_5_text = level_5.find('b').text.strip() if level_5 and level_5.find('b') else "N/A"

        data.append([level_1_text, level_2_text, level_3_text, risk_score, level_5_text])

    return data


def scrape_all_levels():
    os.makedirs("datasets", exist_ok=True)
    all_data = []

    for level in range(1, 6):
        for page in range(1, max_pages + 1):
            data = scrape_page(level, page)
            if data:
                all_data.extend(data)
            else:
                skipped_pages.append((level, page))

        # Save to CSV
        df = pl.DataFrame(all_data, schema=["Category", "Attack Name", "Description", "Risk Score", "Date"])
        df.write_csv(f"datasets/forti_lists_{level}.csv")

    # Save skipped pages
    with open("datasets/skipped.json", "w") as f:
        json.dump(skipped_pages, f, indent=4)


scrape_all_levels()
driver.quit()
