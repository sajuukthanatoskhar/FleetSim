import socket
import sys
import codecs

if __name__=="__main__":
    hostip= "127.0.0.1"
    hostport = 6790
    clientport = 6789
    initialMessage = "fleetplayer,sajuuk"

    playerclients_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)


    playerclient_toserver = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    playerclient_toserver.sendto("fleetplayer,sajuuk".encode("utf-8"),(hostip,clientport))