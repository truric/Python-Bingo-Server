import socket
from _thread import *

# Instead of hard coding an IP address, here we are getting and setting the ip address of the machine running the app.
server = socket.gethostbyname(socket.gethostname())
# Any port you choose, must be the same on server.py and client.py. Same goes to the IP.
port = 5555

# IP and port done, now we need to make a socket that will allows us to open to other connections.
# Once the socket is created, we need to bind the socket to the address.
# socket.AF_INET: type of address set to IPv4.
# socket.SOCK_STREAM: this will allow data to be sent through the socket.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # The socket is now bound to this address, anything that connects to this address will hit this socket.
    s.bind((server, port))
    # The socket becomes passive and will be accepting incoming connections requests.
    s.listen(3)
except socket.error as err:
    str(err)

print("Waiting for connection. \nServer Started at {}:{}".format(server, port))


def threaded_client(conn, addr):
    conn.send(str.encode(f"New connection from: {addr}"))
    reply = ""
    while True:
        try:
            # Wait until something is sent to this socket.
            # 2048 is in bytes, as I need to give a fixed number, 2048 will be enough for any message to be passed
            data = conn.recv(2048)
            # Will decode this message format from bytes in to a string.
            reply = data.decode("utf-8")

            if not data or reply == "exit":
                print("Disconnected")
                break
            else:
                print("Message from Client: ", reply)

            conn.sendall(str.encode(reply))
        except:
            break

    print("Lost connection")
    conn.close()


while True:
    # It will wait until a new connection to the server.
    # Once that connection occurs, the address will be stored (ip and port)
    # and a new socket object conn that can be used to send and receive data through threaded_client()
    conn, addr = s.accept()
    print("Connected to:", addr)
    start_new_thread(threaded_client, (conn, addr))

    # As I understood, there's different ways to do this for different versions of Python.
    # This is a different approach to achieve the same goal.
    # thread = threading.Thread(target=threaded_client(conn), args=(conn, addr))
    # thread.start()