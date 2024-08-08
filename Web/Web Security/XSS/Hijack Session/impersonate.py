import urllib.parse
import requests

session_data = "RETRIEVED_SESSION"
method = "GET"
site = "http://challenge.localhost"
url = f"{site}/info?user=1"

# Set the headers with the session cookie
headers = {'Cookie': f'session={session_data}'}

response = requests.request(method, url, headers=headers)

print(f"Flag: {response.text}")
