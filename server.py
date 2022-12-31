import random
import socket
import threading
import json 


#Variables for holding information about connections
connections = []
total_connections = 0
tempConnections = 0
senderToReceiver = {}
idToName = {}
#dummy gifts dictionary
giftsDict = {"1" : "bag",
                   "2" : "ball",
                   "3" : "bicycle"}
isFinished = False

isGameStarted = False
   
   
class Client(threading.Thread):
    
    
    #Client class, new instance created for each connected client
    #Each instance has the socket and address that is associated with items
    #Along with an assigned ID and a name chosen by the client
    
    def __init__(self, socket, address, id, name, signal):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.id = id
        self.name = name
        self.signal = signal
    
    def __str__(self):
        return str(self.id) + " " + str(self.address)
    
    
    
    #Attempt to get data from client
    #If unable to, assume client has disconnected and remove him from server data
    #If able to and we get data back, print it in the server and send it back to every
    #client aside from the client that has sent it
    #decode is used to convert the byte data into a printable string

    def run(self):
       
    
  
        ##variables to check the status of the game to prevent malicious actions
        #tempConnections is used to check if all the clients have sent their gifts correctly
        global isGameStarted
        global tempConnections
        
        while self.signal:
            try:
                data = self.socket.recv(256)
                decodedData = str(data.decode("utf-8"))
                print(decodedData)
            except:
                print("Client " + str(self.address) + " has disconnected")
                self.signal = False
                connections.remove(self)
                break
            
            
           
            #if the user is trying to cheat, disconnect him and send a message to all other clients
            if isGameStarted == False and "please choose one gift and write its number" in str(data.decode("utf-8")):
                
                self.socket.sendto(str.encode(json.dumps(f"you are a sheeetar!!!!")) , self.address)
                print("Client " + str(self.address) + " has disconnected")
                for client in connections:
                    if client.id != self.id:
                        client.socket.sendall(str.encode(f"client {self.id} is a sheeetaar!!!! and therefore has been diconnected"))
                self.signal = False
                connections.remove(self)
                self.address = None
                self.id = None
                self.signal = None
                self.socket = None
                tempConnections -= 1
                total_connections -= 1
                break
            
            #the game starts here after any client sends the message "start user distribution"   
            elif (str(data.decode("utf-8")) == "start user distribution" and isGameStarted == False):
                isGameStarted = True
                
                #the function that distributes the users to each other
                distributePeople(connections)
                #inform every client with the user he will send a gift to and ask him to choose a gift
                for client in connections:
                        recieverId = int(senderToReceiver[client.id][0]) 
                        client.socket.sendto(str.encode(json.dumps(f"You will send a gift to {idToName[recieverId]} ")) , client.address)
                        client.socket.sendall(str.encode(f"please choose one gift and write its number from {json.dumps(giftsDict)}"))
                     
                        
            #the client sends the gift he chose to send to the user he was assigned to send it to
            elif("The gift i choose is" in str(data.decode("utf-8"))):
                #check if he has sent a gift from the dictionary(valid gift)
                #if he did not chose a gift from the dictionary, ask him to choose a gift from the dictionary
                if(decodedData[23:] not in giftsDict):
                    self.socket.sendto(str.encode(json.dumps(f"please send a gift from the dictionary! please choose one gift and write its number")) , self.address)
                #if he chose a gift from the dictionary, send him a confirmation message and add the gift to the list of gifts he will send
                else:
                    recieverId = senderToReceiver[self.id][0]
                    self.socket.sendto(str.encode(json.dumps(f"the gift you'll send is a {giftsDict[decodedData[23:]]} to client {idToName[int(recieverId)]}")) , self.address)
                    giftName = [giftsDict[decodedData[23:]]]
                    senderToReceiver[self.id] = senderToReceiver[self.id]+giftName
                    tempConnections -= 1
                    #if we reaches this point, it means that all the clients have chosen their gifts
                    if(tempConnections == 0):
                        #if we enter here, the server will send the gifts to the corresponding clients
                        for sender, recAndGift in list(senderToReceiver.items()):
                            print(senderToReceiver.values())
                            receiver = int(recAndGift[0])
                            gift = recAndGift[1]
                            #send the gift to the client and inform him with the sender
                            for client in connections:
                                if receiver == client.id:
                                    client.socket.sendto(str.encode(f"you have received a gift: {gift} from client {idToName[int(sender)]}") , client.address)
                                    
                                    #inform every client that the game has ended
                                    client.socket.sendto(str.encode("the game has ended") , client.address)
                                    client.socket.sendto(str.encode("please disconnect") , client.address)
                       
                        
                           
            #Here is the server append the client name to his id to use it in further messages
            elif decodedData.startswith("#"):
                self.name = decodedData[1:]
                idToName[self.id] = self.name
            
                                
            #if the client sends a message, broadcast it.                    
            elif data != "":
                print("ID " + str(self.id) + ": " + decodedData)
                for client in connections:
                    if client.id != self.id:
                        client.socket.sendall(data)

#Wait for new connections
def newConnections(socket):
    while True:
        sock, address = socket.accept()
        global total_connections
        global tempConnections
        connections.append(Client(sock, address, total_connections, "Name", True))
        connections[len(connections) - 1].start()
        print("New connection at ID " + str(connections[len(connections) - 1]))
        total_connections += 1
        tempConnections += 1

def main():
    #Get host and port
    host = "localhost"
    port = int(3000)
    #Create new server socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(5)

    #Create new thread to wait for connections
    newConnectionsThread = threading.Thread(target = newConnections, args = (sock,))
    newConnectionsThread.start()
    
main()


#creat dictionary to assign connection ids as senders which then randomizes the senders and receivers and later assigns each sender one receiver(1:1 mapping)
#each sender must have 1 receiver but the receiver does not have to send a gift to his sender

#this method makes sure that every client will have a receiver and that no client will send a gift to himself
#it also makes sure that every client will send a gift to another client
def distributePeople(connections):
    global senderToReceiver

    
    for client in connections:
        senderToReceiver[client.id] = ""

    sendersList = list(senderToReceiver.keys())
    receiversList = list(senderToReceiver.keys())

    while (len(sendersList) != 0 and len(receiversList) != 0):    
        randomSender = random.choice(sendersList)
        randomReceiver = random.choice(receiversList)

        if len(sendersList) == 2:
            commonSet = set(sendersList).intersection(receiversList)
            commonList = list(commonSet)
            if(len(commonList) == 2):
                senderToReceiver[sendersList[0]] = [f"{receiversList[1]}"]
                senderToReceiver[sendersList[1]] = [f"{receiversList[0]}"]
                break
            elif(len(commonList) == 0):
                senderToReceiver[randomSender] = [f"{randomReceiver}"]
            
            else:
                for i in range(len(sendersList)):
                    for j in range(len(receiversList)):
                        if(sendersList[i] == sendersList[j]):
                            if((i == 1 and j == 1) or (i == 0 and j == 0)): #[0 , 2] [1 , 2] ||||||| [0 , 1] [0 , 2]
                                senderToReceiver[sendersList[1]] = [f"{receiversList[0]}"]
                                senderToReceiver[sendersList[0]] = [f"{receiversList[1]}"]
                                isFinished = True
                                break
                            elif((i == 1 and j == 0) or ((i == 0 and j == 1))): #[0 , 1] [1 , 2] ||| [3 , 4] [2 , 3]
                                senderToReceiver[sendersList[0]] = [f"{receiversList[0]}"]
                                senderToReceiver[sendersList[1]] = [f"{receiversList[1]}"]
                                isFinished = True
                                break
                    if isFinished:
                        break
                if isFinished:
                    break
                    
        
        elif randomReceiver != randomSender:
            senderToReceiver[randomSender] = [f"{randomReceiver}"]
        else:
            continue
        sendersList.remove(randomSender)
        receiversList.remove(randomReceiver)
        
        print(sendersList)
        print(receiversList)
    print(senderToReceiver)


#[0 , 1]
#[1 , 2]
#[2 , 0]

#------------------------------------

#[0 , 1 , 1 , 2]
#or
#[0 , 2 , 1 , 2]

#------------------------------------


 #[0 , 2]
            #[1 , 2] handled

            #[0 , 2]
            #[0 , 2]

            #[0 , 1]
            #[1 , 2]

            #[0 , 1]
            #[0 , 2]

            #[3 , 4]
            #[2 , 3]

            #[0 , 1 , 2 , 3 , 4 , 5]
            #[0 , 1 , 2 , 3 , 4 , 5]
        