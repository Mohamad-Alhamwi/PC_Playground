from requests import request

method = "GET"
site = "http://challenge.localhost"
port = 80
params = {"path": "/flag"}

url = f"{site}:{port}/"

response = request(method, url, params = params)

print(f"\nResponse: {response.text}")
