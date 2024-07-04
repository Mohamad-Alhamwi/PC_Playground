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
json_data = {"a":"1f9c3ee48c66402c708741fc61fafdc3", "b":{"c": "dbde341d", "d": ["edae93cf", "9a09d568 7b377554&47171422#8e744df5"]}}

# Set required headers.
headers = {'Host':'4a73dc60f61ee46957e6a4437c128754', 'Content-Type':'application/json'}

response = requests.request(method, url, headers=headers, json=json_data)

print(response.text)