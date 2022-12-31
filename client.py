import socket
import threading
import sys

decodedData = ""


#Wait for incoming data from server
#.decode is used to turn the message in bytes to a string
def receive(socket, signal):
    while signal:
        
        try:
            data = socket.recv(256)
            global decodedData
            decodedData = str(data.decode("utf-8"))
            print(decodedData)
            if signal == False:
                break
        except:
            print("You have been disconnected from the server")
            signal = False
            break

#Get host and port
host = "localhost"
port = int(3000)


#Attempt connection to server
try:
    #input = input("Enter your name: ")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
except:
    print("Could not make a connection to the server")
    input("Press enter to quit")
    sys.exit(0)

#Create new thread to wait for data
receiveThread = threading.Thread(target = receive, args = (sock, True))
receiveThread.start()

#Send data to server
#str.encode is used to turn the string message into bytes so it can be sent across the network
while True:
    message = input()
    if("please choose one gift" in decodedData):
        sock.sendall(str.encode(f"The gift i choose is a {message}"))
    elif("you are a sheeetar" in decodedData):
        sock.sendall(str.encode("i am the worst sheetar in the GIU"))
        break    
    else:
        sock.sendall(str.encode(message))
    

