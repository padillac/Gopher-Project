#This program runs a Gopher server that allows the user to publish a directory of content over the internet to all Gopher users.
#Written by Chris Padilla, Python 3.6.2 4/12/18


import sys, socket
from threading import Thread


#This function defines the servers state while it is waiting to receive a TCP connection
def passive(serverSocket):
    try:
        serverSocket.listen()
        print("Server is listening...\n")
        clientSocket, clientAddr = serverSocket.accept()
        return clientSocket, clientAddr
    except OSError as ose:
        print("Server socket closed.")

#A helper method that returns the contents of a text file, used to quickly read files that the client requests.
def readFromFile(f):
    inFile = open(f)
    data = inFile.read()
    inFile.close()
    return data

#This is the central function of the server: it takes in a selector (received over the TCP connection)
#and returns the data that is being requested, whether that data is a file or a .links directory.
def getData(selector):
    data = "Unrecognized request. Closing connection."
    #sends links file or requested data.
    selector = selector.strip()
    if selector == "\n" or selector == "" or selector == ".":
        data = readFromFile("dir/.links.txt") #filename had to be changed to "links.txt" on mac lab computers
    elif selector[-1] == "/":
        changeDir = selector.strip()
        print(changeDir)
        data = readFromFile(changeDir + ".links.txt")

    else:
        selector = selector.strip()
        try:
            data = readFromFile(selector)
        except FileNotFoundError as f:
            data = "File Not Found -- Client requested: " + selector
            print(data)
        except OSError as o:
            data = "Error retrieving file: " + selector
            print(data)

    data = data + "\n."
    return data

#This function describes the actions the server takes when it receives a TCP connection
def respond(sock):
    #First receive the request from the client.
    messageReceived = sock.recv(4096).decode()
    while messageReceived != "" and messageReceived[-1] != "\n":
        messageReceived = messageReceived + sock.recv(4096).decode()
    print("Message from Client: " + messageReceived)
    #Reply to the client with the requested data, using the getData() method
    message = getData(messageReceived)
    print("\nSENDING MESSAGE:\n" + message)
    sock.send(message.encode()) #send requested info/file
    #Closes connection to client after one transaction
    sock.close()
    print("\nClosed connection to client.\n")


def main():
    #initialize server
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    hostName = ""
    port = 60000
    serverSocket.bind((hostName, port))
    #Two functions that allow the server to be quit.
    def exitFunction():
        while input("Enter 'q' to exit: ") != "q":
            pass
        killSocket(serverSocket)
    def killSocket(s):
        s.close()
    #This thread allows the user to interrupt the server processes to quit the program.
    thread = Thread(target = exitFunction, args = ())
    thread.start()

    while thread.is_alive():
        try:
            clientSocket, clientAddr = passive(serverSocket)
            print("\nConnection received from: " + str(clientAddr))
            respond(clientSocket)
        except TypeError as te:
            pass

main()
