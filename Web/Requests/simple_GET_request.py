import requests
import urllib.parse

# Set up essential request information.
host = "http://127.0.0.1"
port = 80
method = "GET"

# URL-encode the path.
path = "/00333df5 a1a471cd/e7946145 d73d37ef"
encoded_path = urllib.parse.quote(path)  

# Construct the URL.
url = f'{host}:{port}{encoded_path}'

# URL-encode the query parameters.
params = {'a':'967a38653aa1f9ec9e1f299d83ce3a1b', 'b':'f9fd3a63 99afcc65&3f901d59#21d742cc'}

# Set required headers.
headers = {'Host':'4a73dc60f61ee46957e6a4437c128754'}

response = requests.request(method, url, headers=headers, params=params)

print(response.text)
