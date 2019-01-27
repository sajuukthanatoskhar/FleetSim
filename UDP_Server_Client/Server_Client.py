import socket
import sys

UDP_IP_Address= "127.0.0.1"
print(sys.argv[1])
if(int(sys.argv[1]) == 0):
    UDP_port_no = 6789
    SenderPort = 6790
elif (int(sys.argv[1]) == 1):
    UDP_port_no = 6790
    SenderPort = 6789
Message = "hello"

clientsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


serversock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serversock.bind((UDP_IP_Address,UDP_port_no))

clientsock.sendto("hello".encode("utf-8"), (UDP_IP_Address,SenderPort))

while True:
    data,addr = serversock.recvfrom(1024)
    data = data.decode("utf-8")
    print("Message: %s" % data)

    if(data == "hello"):
        clientsock.sendto("how are you?".encode("utf-8"),(UDP_IP_Address,SenderPort))
    if(data == "how are you?"):
        clientsock.sendto("good?\n".encode("utf-8"), (UDP_IP_Address, SenderPort))
        clientsock.sendto("how are you?".encode("utf-8"), (UDP_IP_Address, SenderPort))
m