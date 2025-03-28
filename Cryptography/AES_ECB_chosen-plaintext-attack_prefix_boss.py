#!/bin/python3

from pwn import *
from requests import request

context.arch = 'amd64'

challenge_file = "CHALLENGE_FILE"
ps = process(challenge_file)
GREEN = "\033[92m"
RED = "\033[95m"
RESET = "\033[0m"
     
def issueRequest(method="GET", query_param=None, query_value=None, path='/'):

    host = "http://challenge.localhost"
    port = "80"
    url = f"{host}:{port}{path}"

    if method == "POST":
        data = {query_param: query_value}
        response = request(method, url, data = data).text
    else:
        params = {query_param: query_value}
        response = request(method, url, params = params).text

    return response

def getSecret(response):
    ## Extract the secret.
    secret_line = response.split('\n')[5]
    unparsed_secret = secret_line.split('<pre>')[-1].split('</pre>')[0]
    parsed_secret = base64.b64decode(unparsed_secret)

    blocks = [parsed_secret[i:i+16] for i in range(0, len(parsed_secret), 16)]

    print("\n")
    for counter, block in enumerate(blocks):
        print(f"Block #{counter} {block}")
    
    if blocks[0] == blocks[5]:
        return True

    return False         

def pickOperation(operation, data=None):
    if operation == 1:
        response = issueRequest()
    elif operation == 2:
        response = issueRequest("POST", "content", data)
    elif operation == 3:
        response = issueRequest("POST", path = "/reset")
    else:
        print("No such operation!")
    
    return response

def main():
    flag = ''
    
    ## One will be added to account for the | character. So in reality you are prefixing by 8. 
    ## The 5th block starts showing up at the 7th character, but you need to account for the padding block so start from the 8th one.
    for counter in range(7, 64):
        ## Loop through ASCII printable chars.
        for ascii_value in range(32, 127):
            block_size = 16
            prefix = 'A' * counter

            if len(flag) < 16:
                fragment = chr(ascii_value) + flag
            
            else:
                fragment = chr(ascii_value) + flag[0:15]

            pad_len = block_size - len(fragment)
            my_input = fragment + (chr(pad_len) * pad_len) + prefix

            is_found = getSecret(pickOperation(2, my_input))
            if is_found:
                print(f"{RED}Found Character: {chr(ascii_value)}{RESET}")
                flag = chr(ascii_value) + flag
                break
            
            pickOperation(3)
               
    print(f"\n{GREEN}{flag}{RESET}")

if __name__ == "__main__":
    main()
