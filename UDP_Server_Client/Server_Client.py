import socket
import sys
import codecs

def receive_packet(socket_sock):
    packet,addr = socket_sock.recvfrom(1024)
    return packet.decode("utf-8")

def send_packet(socket_sock,packetdata,UDP_IP,destination_port): #if -1
#    packetdata = input(str(reason))
    state = socket_sock.sendto(str(packetdata).encode("utf-8"),(UDP_IP,destination_port))
    print(str(packetdata).encode("utf-8"))
    return state

if __name__=="__main__":
    hostip= "127.0.0.1"
    print(sys.argv[1])
    if(int(sys.argv[1]) == 0):
        hostport = 6789
        clientport = 6790
    elif (int(sys.argv[1]) == 1):
        hostport = 6790
        clientport = 6789
    Message = "hello"

    clientsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


    serversock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serversock.bind((hostip, hostport))

    clientsock.sendto("hello".encode("utf-8"), (hostip, clientport))
    state = -1
    while True:
        state = receive_packet(serversock)
        print(str(state))
        if (state == 3):
            pass #what happens here?

        # data,addr = serversock.recvfrom(1024)
        while(state == 'wait-state'):
            valid_options = {'1','5','4'}
            state = input("Menu\n1.\tChange Targets for which fleet against which fleet\n5.\tMove to certain spot with anchor\n4.\tMove to next round\n")
            if state in valid_options:
                print("Valid option")
                if state == '5':
                    X = input("X coordinate? ")
                    Y = input("Y coordinate? ")
                    Z = input("Z coordinate? ")
                    fleet = input("Fleet name? ")

                    state = str(state + " " + X + " " + Y + " " + Z + " " + fleet)
                    clientsock.sendto(state.encode("utf-8"), (hostip, clientport))
                    state = 'wait-state'
                    continue
                if state == '4':
                    clientsock.sendto(state.encode("utf-8"), (hostip, clientport))
                    state = 'wait-state'
                    print("Continuing on...")
                    break


            else:
                print("\nError + " + str(state))
                state = 'wait-state'
                continue

            clientsock.sendto(state.encode("utf-8"),(hostip,clientport))
            print("breaking back to previous while - state = " + state)
            #send_packet(clientsock, state, hostip, clientport)
            #clientsock.sendto(state.encode("utf-8"),(UDP_IP_Address,SenderPort))

        # data = data.decode("utf-8")
        # print("Message: %s" % data)
        #
        # if(data == "hello"):
        #     clientsock.sendto("how are you?".encode("utf-8"),(UDP_IP_Address,SenderPort))
        # if(data == "how are you?"):
        #     clientsock.sendto("good?\n".encode("utf-8"), (UDP_IP_Address, SenderPort))
        #     clientsock.sendto("how are you?".encode("utf-8"), (UDP_IP_Address, SenderPort))
