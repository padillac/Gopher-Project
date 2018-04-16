#This program allows the user to interact with Gopher servers in an intuitive and simple way.
#Writen by Chris Padilla, Python 3.6.2, 4/12/18


import sys, socket

#prints this error message if the user provides bad arguments.
def usage():
    print ("Usage: python GopherClient.py server port")

#Helper method that connects to a given server on a given port.
def socketConnect(server, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((server, port))
        return sock
    except ConnectionRefusedError as cre:
        print("The server host refused the connection.\nMake sure the server is running.\n")

#Helper method that sends a given string to a socket
def sendRequest(s,data):
    s.send(data.encode())

#Central method of the client, which processes data received from the server
#to display in a user-friendly way to the user.
def parseData(message, s, l):
    lines = message.split("\n")
    entries = []
    looper = l
    for line in lines:
        if len(line.split("\t")) >= 4:
            entries.append(Entry(line, looper))
            looper += 1
        elif line != "" and line != ".":
            print("Could not evaluate line:\n'" + line + "'")
    if lines[len(lines)-1] != ".":
        try:
            sendRequest(s,"\n")
            moreData = s.recv(8192).decode()
            entries = parseDataHelper(moreData, s, entries, looper)
        except ConnectionAbortedError:
            1+1
        except RecursionError as re:
            1+1


    return entries

#Recursive helper method for parseData() to account for some Gopher servers
#sending data in chunks for some reason. This ensures that the client receives all data.
def parseDataHelper(message, s, entries, l):
    moreEntries = parseData(message, s, l)
    newEntries = entries
    for each in moreEntries:
        newEntries.append(each)

    return newEntries



#Method that displays directory data sent by the server in a user-friendly way.
def formatData(entries):
    displayString = ""
    for each in entries:
        displayString = displayString + each.toString() + "\n"

    return displayString

#class that stores information about data sent by the server in a modular way,
#allowing the user to easily select entries and navigate the Gopher server.
class Entry:
    def __init__(self, line, num):
        info = line.split("\t")
        self.number = num
        self.name = info[0][1:]
        self.selector = info[1]
        self.server = info[2]
        self.port = info[3]
        self.type = ""
        if info[0][0] == "0":
            self.type = "FILE"
        elif info[0][0] == "1":
            self.type = "DIRECTORY"
        else:
            self.type = "UNKNOWN"

    def toString(self):
        objString = str(self.number) + " - " + self.type + ": " + self.name
        return objString

    def getSelector(self):
        return self.selector

    def getType(self):
        return self.type

#Another central function of the client, that takes in raw input given by the user
#and returns either a usage error or a correctly formatted message that conforms to Gopher
#protocol to be sent to the server.
def craftMessage(userInput, entries):
    message = "VOID"
    typeOfRequest = ""

    if userInput == "" or userInput == ".":
        message = "\n"
        typeOfRequest = "DIRECTORY"
    else:
        try:
            userSelection = int(userInput)
            message = entries[userSelection-1].getSelector() + "\n"
            typeOfRequest = entries[userSelection-1].getType()
        except IndexError as i:
            print("Invalid choice, please select an option by its number.")
        except ValueError as v:
            print("Invalid input, please enter an integer, or press ENTER to display files.")

    return message, typeOfRequest

#Main function of client, that manages the order of interactions between user, client, and server.
def main():
    print()
    if len(sys.argv) == 3:
        try:
            server = sys.argv[1]
            port = int(sys.argv[2])
        except ValueError as e:
            usage()

        #Test if user input represents a valid server.
        sock = socketConnect(server, port)
        if type(sock) == socket.socket:
            print("Connected to:\nServer: " + server + "\nPort: " + str(port))
            sock.close()
        else:
            print("Failure connecting to:\nServer: " + server + "\nPort: " + str(port) + "\nPlease try again.\n\nNow exiting program.")
            sys.exit()

        #initialize main loop of client
        print("Press enter to display the contents of this server.")
        parsedData = []
        command = input(">>> ")
        #main loop of client
        while command != "exit":
            outMessage, typeOfRequest = craftMessage(command, parsedData)
            if outMessage != "VOID":
                try:
                    sock = socketConnect(server, port)
                    sendRequest(sock,outMessage)
                    response = sock.recv(8192).decode()

                    #handlers for different types of requests
                    if typeOfRequest == "FILE":
                        print("\nFILE REQUESTED\n")
                        print(response)
                        if response.split("\n")[len(response.split("\n"))-1] != ".":
                            try:
                                sendRequest(sock,"\n")
                                moreData = sock.recv(8192).decode()
                                print(moreData)
                            except ConnectionAbortedError:
                                1+1
                    elif typeOfRequest == "DIRECTORY":
                        print("\nDIRECTORY REQUESTED\n")
                        parsedData = parseData(response, sock, 1)
                        display = formatData(parsedData)
                        print(display)
                    else:
                        print("\nUNKNOWN FILE REQUESTED\n")
                        print(response)

                #catch-blocks for a bunch of common connecction errors.
                except ConnectionAbortedError as cae:
                    print("Connection Aborted Error\n")
                except ConnectionResetError as cre:
                    print("The connection was terminated by the remote host.\nPlease try again.\n")
                except AttributeError as ae:
                    print("")
                except UnicodeDecodeError as ude:
                    print("Unable to decode response from server.\n")
                except BrokenPipeError as bpe:
                    print("The connection to the server was lost. Please try again.")
            command = input(">>> ")



    else:
        usage()

main()
