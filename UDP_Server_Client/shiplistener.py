import socket

UDP_IP_Address= "127.0.0.1"

UDP_port_no = 6790

serversock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

serversock.bind((UDP_IP_Address,UDP_port_no))

while True:
    data,addr = serversock.recvfrom(4096)


    data = data.decode("utf-8")

    print("%s" % data)