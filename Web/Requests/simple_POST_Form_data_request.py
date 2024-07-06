import requests
import urllib.parse

# Set essential request information.
host = "http://127.0.0.1"
port = 80
method = "POST"

# URL-encode the path.
path = "/00333df5 a1a471cd/e7946145 d73d37ef"
encoded_path = urllib.parse.quote(path)  

# Construct the URL.
url = f'{host}:{port}{encoded_path}'

# Set body data.
data = {'a':'da0f4a0762eb406c6515df1dc0c20689', 'b':'593cc068 1f6c8fb5&93d95b19#ee9224db'}

# Set required headers.
headers = {'Host':'4a73dc60f61ee46957e6a4437c128754', 'Content-Type':'application/x-www-form-urlencoded'}

response = requests.request(method, url, headers=headers, data=data)

print(response.text)
