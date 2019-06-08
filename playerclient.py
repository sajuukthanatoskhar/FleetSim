import socket
import sys
import codecs
import random
import sys
import os


def noanchor(data):
    count = 0
    choice = 0
    newdata = data[1].split('\n')
    while(choice != -1):
        for i in range(1,len(newdata)-1):
            count += 1
            print("%s %s"% (count,newdata[i]))
        choice = input("What is your next primary? $ ")


def noprimary(data):
    count = 0
    choice = -1
    newdata = data[1].split('\n')
    while(choice == -1):
        for i in range(1,len(newdata)-1):
            count += 1
            print("%s %s"% (count,newdata[i]))
        choice = input("What is your next primary? $ ")
        if int(choice) >= 1 and int(choice) <= len(newdata)-1:
            print("Primary chosen - %s" % newdata[int(choice)])
            choice = newdata[int(choice)].split(" ")[6]  #we return the hex address of the objects
            break
        else:
            choice = -1
    return choice


if __name__=="__main__":
    hostip= "127.0.0.1"
    hostport = random.randint(6700,10000)
    clientport = 6789
    name = sys.argv[1]
    initialMessage = "fleetplayer,%s,%s" % (name,str(hostport))
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
        if int(int(choice) == -2):
            break

    choice = -1
    #while (choice != -2):
    print("Second Phase - Waiting")
    #    data,addr = playerlistenerclient.recvfrom(1024)
        # if int(data.decode('utf-8')) == -2:
        #     break
        # else:
        #     print("Error")


    player_capitulation_status = 0
    while player_capitulation_status == 0:
        if os.name == 'nt':
            _ = os.system('cls')
        print("Capitulation State 0")
        data, addr = playerlistenerclient.recvfrom(1024)
        #todo:check that the addr is the server (lol)
        print(data.decode("utf-8"))
        data = "0"
        while(data!= "ENDGAME"):
            originaldata, addr = playerlistenerclient.recvfrom(10000)
            print(originaldata.decode("utf-8"))
            data = str(originaldata.decode("utf-8")).split(":")
            print("Total: %d Actual String:%s"% (len(data),data))
            if data[0] == "End":
                print("End")
            if data[0] == "NoAnchor":
                print("NoAnchor")
                choice = noanchor(data)
                playerclient_toserver.sendto(choice.encode("utf-8"), (hostip, clientport))
            if data[0] == "NoPrimary":
                print("NoPrimary")
                choice = noprimary(data)
                playerclient_toserver.sendto(choice.encode("utf-8"), (hostip, clientport))
            if data[0] == "Status Update":
                #print("Status Update")
                print(originaldata)
            if data[0] == "StatusCap":
                print("Status Update")                
            responsecmd = input("Send p to continue $ ")
            playerclient_toserver.sendto(responsecmd.encode("utf-8"), (hostip, clientport))



    #todo: then wait for question regarding
    #todo: player then sends fleet
    #todo: server will ask if there is another fleet? ~for v1.1~
    #todo: player sends yes or no - ~for v1.1~

