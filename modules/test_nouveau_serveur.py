import socket

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.bind(('',15555))

while True:
    tcp.listen(2)
    client, address = tcp.accept()
    print(address, "connected")

    recv = client.recv(2048)
    if recv != "":
        print(recv)

print("bye")
client.close()
tcp.close()