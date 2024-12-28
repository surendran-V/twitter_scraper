from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import pymongo
import uuid
from selenium.webdriver.chrome.options import Options
from config import Config
import time

# MongoDB setup
client = pymongo.MongoClient(Config.MONGODB_URI)
db = client["trending_topics"]
collection = db["trends"]

def scrape_twitter_trends():
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--headless")  # Add headless mode for server deployment
    
    driver = webdriver.Chrome(options=chrome_options)
    trends = []
    
    try:
        # Go to Twitter login page
        driver.get("https://twitter.com/login")
        wait = WebDriverWait(driver, 50)
        
        # Input username/email
        username_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[autocomplete='username']"))
        )
        username_input.send_keys(Config.TWITTER_USERNAME)
        
        # Click Next button
        next_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']"))
        )
        next_button.click()
        
        # Input password
        password_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']"))
        )
        password_input.send_keys(Config.TWITTER_PASSWORD)
        
        # Click Login button
        login_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Log in']"))
        )
        login_button.click()

        # Rest of your existing scraper.py code remains the same, just replace hardcoded credentials
        # with Config.TWITTER_USERNAME and Config.TWITTER_PASSWORD
        
        try:
            print("Checking for verification code requirement...")
            verification_input = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[autocomplete='one-time-code']"))
            )
            
            print("\nVerification code required!")
            print("Please check your email for the verification code.")
            print("Waiting for up to 300 seconds for code input...")
            
            max_wait_time = 300
            start_time = time.time()
            verification_code = None
            
            while time.time() - start_time < max_wait_time:
                try:
                    verification_code = input("Enter verification code (or press Ctrl+C to cancel): ")
                    if verification_code:
                        break
                except KeyboardInterrupt:
                    print("\nVerification cancelled by user")
                    return []
            
            if not verification_code:
                print("Timeout waiting for verification code")
                return []
                
            print("Submitting verification code...")
            verification_input.send_keys(verification_code)
            
            verify_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='Verify']"))
            )
            verify_button.click()
            
            print("Waiting for verification to complete...")
            time.sleep(10)
            
        except Exception as e:
            print("No verification required or verification element not found")
            print(f"Details: {str(e)}")
        
        print("Navigating to explore page...")
        driver.get("https://twitter.com/explore/tabs/trending")
        time.sleep(5)
        
        print("Waiting for trends to load...")
        trend_elements = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-testid="cellInnerDiv"]'))
        )

        # Process trends (rest of your existing code)
        for i, trend_element in enumerate(trend_elements[:5], 1):
            try:
                trend_text = trend_element.text
                trend_lines = trend_text.split('\n')
                
                rank = next((line.strip() for line in trend_lines if line.strip().isdigit()), str(i))
                
                trend_name = None
                for line in trend_lines:
                    if (line and 
                        not line.strip().isdigit() and 
                        not 'Trending' in line and 
                        not 'posts' in line.lower() and
                        not 'K' in line and
                        not line.strip() == '·'):
                        trend_name = line.strip()
                        break
                
                if not trend_name:
                    trend_name = "Unknown Trend"
                
                posts_count = next((line for line in trend_lines 
                                  if ('K' in line or 'posts' in line.lower()) 
                                  and not 'Trending' in line), "0 posts")
                
                trend_data = {
                    "nameoftrend" + str(i): {
                        "rank": rank,
                        "name": trend_name,
                        "posts": posts_count
                    }
                }
                
                trends.append(trend_data)
                print(f"Found trend {i}: {trend_name} ({posts_count})")
                
            except Exception as e:
                print(f"Error processing trend {i}: {str(e)}")
                trends.append({
                    "nameoftrend" + str(i): {
                        "rank": str(i),
                        "name": "Error fetching trend",
                        "posts": "0 posts"
                    }
                })

        if not trends:
            print("No trends were found!")
            return []
            
    except Exception as e:
        print(f"Error during scraping: {str(e)}")
        return []
    finally:
        driver.quit()
        
    return trends

def save_to_mongodb(trends):
    try:
        record = {
            "_id": str(uuid.uuid4()),
            "timestamp": datetime.now(),
        }
        
        for trend in trends:
            record.update(trend)
        
        collection.insert_one(record)
        return record
    except Exception as e:
        print(f"Error saving to MongoDB: {str(e)}")
        return None