from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import logging
from datetime import datetime

class HanKyungScraper:
    def __init__(self, start_date, end_date):
        self.start_date = datetime.strptime(start_date, "%Y%m%d")
        self.end_date = datetime.strptime(end_date, "%Y%m%d")
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        logging.info("WebDriver initialized.")

    def fetch_page(self):
        try:
            url = "https://www.hankyung.com/all-news/"
            logging.info(f"Fetching URL: {url}")
            self.driver.get(url)
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.nav-link[data-menu-id='economy']"))).click()
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.day-wrap")))
            return self.driver.page_source
        except Exception as e:
            logging.error(f"Error fetching and navigating the page: {e}")
            return None

    def parse_articles(self, page_source):
        soup = BeautifulSoup(page_source, 'html.parser')
        articles = []
        for article in soup.select("div.day-wrap"):
            date_element = article.select_one("strong.txt-date")
            if date_element:
                article_date = datetime.strptime(date_element.text.strip(), "%Y.%m.%d")
                if self.start_date <= article_date <= self.end_date:
                    for item in article.select("li[data-aid]"):
                        title_element = item.select_one("h3.news-tit > a")
                        text_element = item.select_one("p.lead")
                        edit_date_element = item.select_one(".datetime .txt-date")  # Selector for edited date

                        if title_element and text_element:
                            title = title_element.text.strip()
                            href = title_element.get("href")
                            date = date_element.text.strip()
                            article_text = text_element.text.strip()
                            date_edit = edit_date_element.text.strip() if edit_date_element else "No edit date"  # Handle cases where no edit date is provided

                            articles.append({
                                "date": date,
                                "date_edit": date_edit,
                                "href": href,
                                "title": title,
                                "article": article_text
                            })
        return articles

    def get_articles(self):
        page_source = self.fetch_page()
        all_articles = []
        if page_source:
            all_articles = self.parse_articles(page_source)
            logging.info(f"Parsed {len(all_articles)} articles from the economy section")
        self.driver.quit()
        logging.info(f"Scraping completed. Total articles fetched: {len(all_articles)}")
        return all_articles

