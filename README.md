
# File Server

It's a command line application to transfer files between two machines. Client can sent commands to server to get file, send file, and delete file It is created in python using socket API. 

### Requirements
- Python v3.6 or higher

### Running the Application

#### Notes
- This application it not completely secure, so it's not recommended to expose server port to Internet, use Local Network instead.
- It can be tested on a single machine, but that doesn't feel good. Use your friend's computer as second machine.
- Connect both the machines to same local network, can be your mobile hotspot (dw it won't consume your mobile data).
- To find IP Address of a machine,  you can use `ipconfig` command on Windows and `ifconfig` on Linux Systems.

#### Instructions:
- Connect machine A and machine B to your mobile hotspot.
- Run `server.py` on machine A.
- Run `client.py` on machine B.
- Enter the IP Address of Machine A.
- After the connection is established, type `help` to get a list of available commands.
- Now you can use displayed commands to transfer files.

## If you encounter any error or unhandled exceptions, DM me on [twitter](https://twitter.com/priyanshh32) or open an issue.
## Screenshots

![img.png](img.png)
![img_1.png](img_1.png)

## Authors

- [@priyansh32](https://www.github.com/priyansh32) - [twitter](https://twitter.com/priyanshh32)

