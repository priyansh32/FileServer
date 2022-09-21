# server.py

import socket
import sys
import os

global host
global port
global s


def create_socket():
    try:
        global host
        global port
        global s
        host = ''
        port = 12000
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.settimeout(5)
    except socket.error as msg:
        print("Socket creation error: " + str(msg))
        sys.exit()


def bind_socket():
    try:
        print("Binding the port: " + str(port))
        s.bind((host, port))
        s.listen(5)
    except socket.error as msg:
        print("Socket binding error: " + str(msg) + "\n" + "Retrying...")


def socket_accept():
    while True:
        try:
            conn, address = s.accept()
            print("Connection has been established! | " + "IP: " +
                  address[0] + " | Port: " + str(address[1]))
            start_transfer(conn)
            conn.close()
            print("Connection to " +
                  str(address[0]) + ":" + str(address[1]) + " closed")
        except socket.timeout:
            pass
        except KeyboardInterrupt:
            s.close()
            print("Socket has been closed")
            sys.exit()
            # could not properly handle KeyboardInterrupt exception but okay


def get_files_list(conn):
    list_of_files = os.listdir()  # get directory listing
    out = '\n'.join(list_of_files)  # convert to string

    conn.recv(1024)  # sync with client

    msg_size = len(out)

    conn.send(bytes(str(msg_size), "utf-8"))  # send msg size
    conn.recv(1024)  # sync with client

    # send msg
    conn.sendall(bytes(out, "utf-8"))
    conn.recv(1024)  # sync with client


def change_directory(conn):
    data = conn.recv(1024).decode()

    try:
        os.chdir(data)
    except OSError:
        conn.send(bytes("0", "utf-8"))
        return
    conn.send(bytes("1", "utf-8"))
    conn.recv(1024)
    conn.send(bytes(os.getcwd(), "utf-8"))


def print_working_directory(conn):
    conn.recv(1024)
    conn.send(bytes(os.getcwd(), "utf-8"))


def send_file(conn):
    file_name = conn.recv(1024).decode()

    # if file does not exist
    if not os.path.isfile(file_name):
        conn.send(bytes('0', 'utf-8'))
        return

    # ready to send file
    conn.send(bytes('1', 'utf-8'))

    file_size = os.path.getsize(file_name)

    conn.send(bytes(str(file_size), "utf-8"))
    conn.recv(1024)

    # reading file in one go will consume more memory
    # since sending file would require loading file into main memory
    # so, we read file in chunks and send them
    total_sent = 0
    print('Sent: ' + str(round(total_sent / file_size * 100, 2)) + '%')
    with open(file_name, 'rb') as f:
        while True:
            data = f.read(2048)
            if not data:
                break
            conn.send(data)
            total_sent += len(data)
            # print percentage of file sent precision to 2 decimal places
            print('\033[1A' + 'Sent: ' +
                  str(round(total_sent / file_size * 100, 2)) + '%')

    # conn.recv(1024)
    print('\033[1A' + "File sent successfully")


def receive_file(conn):
    # receive file name
    file_name = conn.recv(1024).decode()
    conn.send(bytes("1", "utf-8"))

    file_size = int(conn.recv(1024).decode())
    conn.send(bytes("1", "utf-8"))
    # receive file
    og_file_size = file_size
    total_received = 0
    print('Received: ' + str(round(total_received / og_file_size * 100, 2)) + '%')
    with open(file_name, 'wb') as f:
        while file_size > 0:
            data = conn.recv(2048)
            f.write(data)
            file_size -= len(data)
            total_received += len(data)
            print('\033[1A' + 'Received: ' +
                  str(round(total_received / og_file_size * 100, 2)) + '%')

    # acknowledge
    # conn.send(bytes("1", "utf-8"))
    print('\033[1A' + "File received successfully")


def delete_file(conn):
    file_name = conn.recv(1024).decode()

    try:
        os.remove(file_name)
        conn.sendall(bytes("File deleted", "utf-8"))
    except FileNotFoundError:
        conn.sendall(bytes("Error: File not found", "utf-8"))
    except PermissionError:
        conn.sendall(bytes("Error: Permission denied", "utf-8"))
    except:
        conn.sendall(bytes("Error: Unknown error", "utf-8"))


def start_transfer(conn):
    while True:
        try:
            data = conn.recv(1024).decode()
            conn.send(bytes("1", "utf-8"))

            print(data)
            if data == "ls":
                get_files_list(conn)
            elif data == "cd":
                change_directory(conn)
            elif data == "pwd":
                print_working_directory(conn)
            elif data == "put":
                receive_file(conn)
            elif data == "get":
                send_file(conn)
            elif data == "delete":
                delete_file(conn)
            elif data == "quit":
                break
            else:
                print("Error: Invalid command")
                # break
        except:
            break


def main():
    create_socket()
    bind_socket()
    socket_accept()


if __name__ == "__main__":
    main()
