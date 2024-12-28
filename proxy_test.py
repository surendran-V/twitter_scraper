import requests
from app.config import Config
proxy_url = f"http://{Config.PROXYMESH_USERNAME}:{Config.PROXYMESH_PASSWORD}@us-ca.proxymesh.com:31280"
proxies = {"http": proxy_url, "https": proxy_url}

try:
    response = requests.get("https://www.google.com", proxies=proxies)
    print("Proxy is working. Status code:", response.status_code)
except Exception as e:
    print("Proxy test failed. Error:", str(e))
