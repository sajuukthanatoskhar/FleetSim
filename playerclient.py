import socket
import sys
import codecs
import random
if __name__=="__main__":
    hostip= "127.0.0.1"
    hostport = random.randint(6700,10000)
    clientport = 6789
    initialMessage = "fleetplayer,sajuuk," + str(hostport)
    print(initialMessage)
    playerlistenerclient = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    playerlistenerclient.bind(("",hostport))
    playerclients_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)


    playerclient_toserver = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    playerclient_toserver.sendto(initialMessage.encode("utf-8"),(hostip,clientport))


    #todo: wait for received packet
    data,addr = playerlistenerclient.recvfrom(1024)
    data = data.decode('utf-8')
    choice = -1
    print("ReturnACK : " + str(data))
    if data != None:
        playerclient_toserver.sendto("ok".encode("utf-8"), (hostip, clientport))
    else:
        print("Error")
    while(choice != -2):
        data, addr = playerlistenerclient.recvfrom(1024)
        choice = input(data.decode('utf-8'))
        playerclient_toserver.sendto(choice.encode("utf-8"), (hostip, clientport))
        if int(choice == -2):
            break

    choice = -1
    while (choice != -2):
        print("Second Phase - Waiting")
        data,addr = playerlistenerclient.recvfrom(1024)
        if int(data.decode('utf-8')) == -2:
            break
        else:
            print("Error")





    #todo: then wait for question regarding
    #todo: player then sends fleet
    #todo: server will ask if there is another fleet? ~for v1.1~
    #todo: player sends yes or no - ~for v1.1~

