# Simple HTTP Proxy Server - Enhanced
from socket import *

import sys

#Initialisation Parameters
hostname=gethostname()
IPAddr=gethostbyname(hostname)
print("Detected Server's Hostname is: " + hostname)
print("Detected Server's IP Address is: " + IPAddr)
print("These are the suggested value for running this proxy on this system.")

try:

        serverip = str(input("Enter Server IP or hostname: "))
        tcpSerPort = int(input("Enter a listening port for the HTTP Proxy: "))
except KeyboardInterrupt:
        sys.exit (0)

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)



# Prepare a server socket
#serverip = sys.argv[1] #from argument
print(serverip +":"+ str(tcpSerPort))
tcpSerSock.bind((serverip, tcpSerPort))
tcpSerSock.listen(5)


while True:
    # Start receiving data from the client
    print('HTTP Proxy is Ready...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from: ', addr)
    

    message = tcpCliSock.recv(4096).decode()
    print(message)
    
    # Extract the filename from the given message
    filename = message.split()[1].partition("//")[2].replace('/', '_')
    fileExist = "false"
    try:
        # Check whether the file exists in the cache
        f = open(filename, "r")
        outputdata = f.readlines()
        fileExist = "true"
        print('File Exists!')

        # ProxyServer finds a cache hit and generates a response message
        tcpCliSock.send("HTTP/1.0 200 OK\r\n")
        tcpCliSock.send("Content-Type:text/html\r\n")

        # Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            tcpCliSock.send(outputdata[i].encode())
        print('Read from cache')

        # Error handling for file not found in cache
    except IOError:
        print('File Exist: ', fileExist)
        if fileExist == "false":
            # Create a socket on the proxy server
            print('Creating Socket on the Proxy Server...')
            c = socket(AF_INET, SOCK_STREAM)

            

            hostn = message.split()[1].partition("//")[2].partition("/")[0]
            print('Host Name: ', hostn)
            try:
                # Connect to the socket to port 80
                #fill start 
                c.connect((hostn, 80))
                #fill end
                print('Socket Has Connected to the Host at Port 80')

                c.sendall(message.encode())
                # Read the response into buffer
                buff = c.recv(4096)
                tcpCliSock.sendall(buff)
               
                # Create a new file in the cache for the requested file.
                # Also send the response in the buffer to client socket
                # and the corresponding file in the cache
                tmpFile = open("./" + filename, "w")
                tmpFile.writelines(buff.decode().replace('\r\n', '\n'))
                tmpFile.close()


            except Exception as inst:
                print('An Illegal Request Has Been Performed.')
                print(inst)

        else:
            # HTTP response message for file not found

            tcpCliSock.send("HTTP/1.0 404 Not Found\r\n")
            tcpCliSock.send("Content-Type:text/html\r\n")
            
            
    # Close the socket and the server sockets
    tcpCliSock.close()
tcpSerSock.close()

