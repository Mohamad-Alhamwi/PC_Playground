import requests

# Set up essential request information.
host = "http://127.0.0.1"
port = 80
method = "GET"

# Construct the URL.
url = f'{host}:{port}'

# Issue the request and store the response.
response = requests.request(method, url)

# Check if the response was redirected
if response.history:
    print("Request was redirected.")
    for resp in response.history:
        print(f"Redirected from {resp.url} to {response.url}")
else:
    print("Request was not redirected.")

# Print the final URL and response content
print(f"Final URL: {response.url}")
print("Response content:", response.text)
