#!/bin/python3

from pwn      import *
from requests import request

context.arch = 'amd64'

challenge_file = "CHALLENGE_PROCESS"
ps = process(challenge_file)
GREEN = "\033[92m"
RESET = "\033[0m"
flag = "SOME_FLAG"

## Issue a request.
def issue_request(query_param, query_value):

    host = "http://challenge.localhost"
    port = "80"
    method = "GET"
    params = {query_param: query_value}
    url = f"{host}:{port}"

    ## Extract the secret.
    response = request(method, url, params = params).text
    secret_line = response.split('\n')[5]
    unparsed_secret = secret_line.split('<pre>')[-1]
    #parsed_secret = base64.b64decode(unparsed_secret.split('</pre>')[0])
    parsed_secret = unparsed_secret.split('</pre>')[0]

    return parsed_secret

## Fetch the encrypted fragment of the flag for the given length.
def get_flag_fragment(length):

    query_value = f"SUBSTR(flag , 1, {length})"

    flag_fragment = issue_request("query", query_value)

    return flag_fragment

# Brute-force the flag character by character.
# by gradually building a flag fragment, incrementing the length as we discover new characters.
# We compare the entire fragment of the flag that we know (plus a new guessed character) against the encrypted version of the flag from the server.
def get_flag(flag):
    for length in range(len(flag), 57):
        # Loop through ASCII printable chars.
        for ascii_value in range(32, 127):
            
            # Encrypt the flag + current guessed character.
            fragment = f"{flag + chr(ascii_value)}"
            # Receive the encrypted fragment of the guessed flag.
            encrypted_fragment = issue_request('query', repr(fragment))
            # Get the actual encrypted flag fragment from the server for comparison.
            flag_fragment = get_flag_fragment(length + 1)
            # Compare the encrypted fragments: if they match, we found the correct character.
            if encrypted_fragment == flag_fragment:
                # Append the correct character to the flag.
                flag += chr(ascii_value)
                print(f"Found character: {chr(ascii_value)}")
                break
                
    return flag
        
flag = get_flag(flag)
print(f"\n{GREEN}The flag{RESET}:\n{flag}\n")
