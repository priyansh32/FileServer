# client.py

import socket
import sys
from functions import *


global host
global port
global c

global PATH


def print_path(conn, cmd):
    print(PATH)


def create_socket():
    try:
        global c
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        c.settimeout(1)
    except socket.error as msg:
        print("Socket creation error: " + str(msg))
        sys.exit()


def connect_socket():
    try:
        global host
        global port
        host = input("Enter host: ")
        port = 12000
        c.connect((host, port))
    except socket.error as msg:
        print("Socket connection error: " + str(msg) + "\n")
        sys.exit(1)
        # could not properly handle KeyboardInterrupt exception but okay


def start_communication():
    global PATH

    c.send("pwd".encode('utf-8'))
    c.recv(1024)  # sync with server

    ack(c)  # acknowledge server
    PATH = c.recv(1024).decode()

    while True:
        try:
            cmd_opt = str(input(PATH + " > "))
            cmd = cmd_opt.split(" ")[0]

            if cmd not in valid_commands:
                print("Invalid command")

            elif cmd == 'help':
                get_help(c, cmd_opt)

            elif cmd == "put":
                put_file(c, cmd_opt)

            elif cmd == "get":
                get_file(c, cmd_opt)

            elif cmd == "delete":
                delete_file(c, cmd_opt)

            elif cmd == "cd":
                path = change_directory(c, cmd_opt)
                if path is not None:
                    PATH = path

            elif cmd == "pwd":
                print(PATH)

            elif cmd == "ls":
                list_directories(c, cmd_opt)

            elif cmd == "quit":
                quit_connection(c, "")
                break

        except ConnectionResetError:
            print("Connection reset by server")
            break
        except KeyboardInterrupt:
            quit_connection(c, "")
            break


def main():
    create_socket()
    connect_socket()
    start_communication()


if __name__ == '__main__':
    main()
