# Secret-Santa

Welcome to the Secret Santa Python Server-Client project!

# Introduction:
Secret Santa is a traditional game in which a group of people exchange gifts anonymously. Each person is randomly assigned to another person in the group to give a gift to. In this project, I have implemented a Secret Santa game using Python's socket module and threading module.



# Protocol Description:
The protocol for this Secret Santa game is designed in such a way that it allows a group of clients to connect to a server and participate in the game. The server is responsible for distributing the clients randomly and collecting the gifts that they have chosen. The clients do not know who they are giving a gift to, but the server tells them at the end of the game.

# The protocol is designed as follows:

-The server is started and listens for incoming connections from clients.
-The clients connect to the server and are assigned an ID and a name by the server.
-One of the clients sends a signal to the server saying "start user distribution".
-The server starts distributing the clients randomly and informs each client for whom they will be buying a gift.
-The server suggests some gifts to each client and asks them to choose one gift from a dictionary.
-The server collects the gifts and sends them to the corresponding recipients.
-The server tells each recipient who sent them the gift.
-The game ends after the server has made sure that every client has received and sent a gift.


# Code Structure:
The code for this Secret Santa game is structured as follows:

-server.py: This file contains the code for the server. It handles the connection and communication with the clients and is responsible for distributing the clients and collecting and sending the gifts.
-client.py: This file contains the code for the clients. It handles the connection and communication with the server and is responsible for sending and receiving gifts.

# Running the Code:
To run the code, you will need to have Python 3 installed on your machine.

-Start the server by running the following command:
python server.py

-Run the client by running the following command in a separate terminal window:
python client.py

-Repeat step 2 for each client that you want to connect to the server.

-One of the clients can start the game by sending the message "start user distribution" to the server.

-Before starting the game, every user should enter their name with a "#" before it. For example, "#Alice". This will help the server identify the names of the clients.


# Protocol Description:
-The server will start distributing the users randomly. At the end of the distribution process, each person will be assigned someone to send a gift to. The server will inform each person who they will be giving a gift to, but not vice versa.

-The server will suggest some gifts to each person, and they must choose one gift from the dictionary. The chosen gift will be the one sent to the recipient.

-After making sure that every person has chosen a valid gift, the server will collect the gifts and send them to their corresponding recipients.

-At the end of the game, the server will inform each recipient who sent them the gift.

-After making sure that every client has received and sent their gifts, the server will inform the clients that the game has ended and they can leave.

Note: If a client disconnects during the game, it may cause problems with the game. It would require more advanced techniques from MPC (Multi-Party Computation) to handle this, which is beyond the scope of this code.

# Troubleshooting:
If you are having trouble connecting to the server, make sure that you are using the correct host and port. The host should be "localhost" and the port should be 3000.
If you are having trouble sending or receiving data from the server, make sure that you are using the correct syntax for sending messages. The messages should be in the form of strings, encoded as bytes before being sent.
If you are experiencing other issues with the code, please do not hesitate to reach out for help.

# Future work:
Implement homomorphic encryption at the server to make the protocol more secure.
















