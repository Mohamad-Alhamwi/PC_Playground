import requests

# Set essential request information.
host = "http://127.0.0.1"
port = 80
method = "GET"

# Construct the URL.
url = f'{host}:{port}'

# Set the cookie.
cookies = {"cookie": "0ba51002d8d8cd7e3eb03c727369ed16"}

# Issue the request and store the response.
response = requests.request(method, url, cookies=cookies)

# Print the response.
print(response.text)