# app/scraper.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import requests
import uuid
from datetime import datetime
from app.config import Config

class TwitterScraper:
    def __init__(self):
        self.proxy = f"http://{Config.PROXYMESH_USERNAME}:{Config.PROXYMESH_PASSWORD}@{Config.PROXYMESH_HOST}"
    
    def setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument(f'--proxy-server={self.proxy}')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=chrome_options)
    
    def login_to_twitter(self, driver):
        driver.get("https://twitter.com/login")
        
        # Wait for and fill username
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "text"))
        )
        username_field.send_keys(Config.TWITTER_USERNAME)
        
        # Click next
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']"))
        )
        next_button.click()
        
        # Wait for and fill password
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        password_field.send_keys(Config.TWITTER_PASSWORD)
        
        # Click login
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Log in']"))
        )
        login_button.click()
    
    def get_trending_topics(self):
        driver = self.setup_driver()
        try:
            self.login_to_twitter(driver)
            
            # Wait for trending section
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='trend']"))
            )
            
            # Get trends
            trend_elements = driver.find_elements(By.CSS_SELECTOR, "[data-testid='trend']")
            trends = [elem.text.split('\n')[0] for elem in trend_elements[:5]]
            
            # Get IP address
            ip = requests.get('https://api.ipify.org').text
            
            # Create record
            return {
                "_id": str(uuid.uuid4()),
                "nameoftrend1": trends[0],
                "nameoftrend2": trends[1],
                "nameoftrend3": trends[2],
                "nameoftrend4": trends[3],
                "nameoftrend5": trends[4],
                "datetime": datetime.now(),
                "ip_address": ip
            }
        finally:
            driver.quit()
