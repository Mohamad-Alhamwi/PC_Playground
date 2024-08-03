import urllib.parse
import requests

method = "GET"
site = "http://challenge.localhost"
port = 80

params = {"user": 1}

url = f"{site}:{port}/"

response = requests.request(method, url, params=params)

print(f"\nResponse: {response.text}")
