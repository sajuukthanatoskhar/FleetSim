import socket
UDP_IP_Address= "127.0.0.1"

UDP_port_no = 6789
Message = "hello"

clientsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientsock.sendto("hello".encode(), (UDP_IP_Address,UDP_port_no))



