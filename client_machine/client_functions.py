import os
from shlex import split as split_cmd

valid_commands = ["quit", "ls", "cd", "pwd", "get", "put", "delete"]

help_text = "Commands:\nquit - quit client\n" \
            "ls - list files in current directory\n" \
            "cd <directory path>- change directory\n" \
            "get <filename>- get file\n" \
            "put <filename>- put file\n" \
            "get <filename>- get file\n" \
            "delete <filename>- delete file\n"


# check if command is valid
def check_formatting(cmd_array):
    if len(cmd_array) == 1:
        print("Requires 1 argument")
        return False

    if len(cmd_array) > 2:
        print("unrecognized argument" + cmd_array[2])
        return False

    return True


# acknowledge server response
def ack(conn):
    conn.send("1".encode('utf-8'))


# receive acknowledgement from server
def syn(conn):
    msg = conn.recv(1024).decode()
    if msg == "1":
        return True
    else:
        return False


def get_help(conn, cmd_opt):
    print(help_text)


def put_file(conn, cmd_opt):
    cmd_array = split_cmd(cmd_opt)

    if not check_formatting(cmd_array):
        return

    file_name = cmd_array[1]

    file_size = os.path.getsize(file_name)

    # send put command
    conn.send("put".encode('utf-8'))
    conn.recv(1024)

    # send file name
    conn.send(file_name.encode('utf-8'))
    conn.recv(1024)

    # send file size
    conn.send(bytes(str(file_size), "utf-8"))
    conn.recv(1024)

    total_sent = 0
    print('sent: ' + str(round(total_sent / file_size * 100, 2)) + '%')
    with open(file_name, "rb") as f:
        while True:
            data = f.read(2048)
            if not data:
                break
            conn.send(data)
            total_sent += len(data)
            print('\033[1A' + 'Sent: ' + str(round(total_sent / file_size * 100, 2)) + '%')

    print('\033[1A' + "File sent successfully")


def get_file(conn, cmd_opt):
    cmd_array = split_cmd(cmd_opt)

    if not check_formatting(cmd_array):
        return

    file_name = cmd_array[1]

    conn.send("get".encode('utf-8'))
    conn.recv(1024)

    conn.send(file_name.encode('utf-8'))

    if not syn(conn):
        print("Error: File not found")
        return

    # receive file size
    file_size = int(conn.recv(1024).decode())
    og_file_size = file_size
    ack(conn)

    total_received = 0
    print('Received: ' + str(round(total_received / og_file_size * 100, 2)) + '%')
    with open(file_name, "wb") as f:
        while file_size > 0:
            data = conn.recv(2048)
            f.write(data)
            file_size -= len(data)
            total_received += len(data)
            print('\033[1A' + 'Received: ' + str(round(total_received / og_file_size * 100, 2)) + '%')

    # ack(conn)
    print('\033[1A' + "File received successfully")


def delete_file(conn, cmd_opt):
    cmd_array = split_cmd(cmd_opt)
    if not check_formatting(cmd_array):
        return

    conn.send("delete".encode('utf-8'))
    conn.recv(1024)

    file_name = cmd_array[1]
    conn.send(file_name.encode())
    msg = conn.recv(1024).decode()
    print(msg)


def change_directory(conn, cmd_opt):
    cmd_array = split_cmd(cmd_opt)

    if not check_formatting(cmd_array):
        return None

    conn.send("cd".encode('utf-8'))
    conn.recv(1024)

    conn.send(cmd_array[1].encode('utf-8'))

    if not syn(conn):
        print("Error: Directory not found")
        return None

    conn.send("1".encode('utf-8'))
    path = conn.recv(1024).decode()
    return path


def list_directories(conn, cmd_opt):
    conn.send("ls".encode('utf-8'))  # client sends the command
    conn.recv(1024)  # server says I have received the command

    ack(conn)  # client says, okay now send the msg size

    msg_size = int(conn.recv(1024).decode())  # server sends the msg size
    ack(conn)  # client says, okay I read the msg size, now send the msg

    msg = conn.recv(msg_size).decode()  # server sends the msg
    ack(conn)  # client says, okay I read the msg

    print(msg)


def quit_connection(conn, cmd_opt):
    conn.send("quit".encode('utf-8'))
    conn.recv(1024)
    conn.close()
    print("Connection closed")
    exit(0)


