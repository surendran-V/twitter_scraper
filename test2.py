from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

proxy = "http://<PROXYMESH_USERNAME>:<PROXYMESH_PASSWORD>@us-ca.proxymesh.com:31280"
chrome_options = Options()
chrome_options.add_argument(f'--proxy-server={proxy}')
service = Service(executable_path="<PATH_TO_CHROMEDRIVER>")

try:
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get("https://www.google.com")
    print("Page title:", driver.title)
except Exception as e:
    print("Error:", e)
finally:
    driver.quit()
