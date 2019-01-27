import socket


UDP_IP_Address= "127.0.0.1"

UDP_port_no = 6789

serversock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

serversock.bind((UDP_IP_Address,UDP_port_no))

while True:
    data,addr = serversock.recvfrom(1024)
    print("Message: %s" % data)