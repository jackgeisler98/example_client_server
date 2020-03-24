import socket                                                   #import library for socket programming
from socket import *                                            #import to use AF_INET 
import sys                                                      #import to use python
import math                                                     #import to perform math operations
import time                                                     #import to use sleep funciton

serverName = '192.168.0.192'                                        #set IP address to connect to (string)
serverPort = 12001                                              #set server port number to connect to
clientSocket = socket(AF_INET, SOCK_STREAM)                     #initialize clientSocke, used throughout code

#function for swtiching ports if current port does not return anything
def nextport():
    clientSocket.close()                                        #close current socket, as another will be opened
    serverPort = serverPort + 1                                 #increment port to try the next one
    if serverPort == 12006:                                     #check to see if it has incremented too many ports, reset to try first one again
        serverPort = 12001
    clientSocket = socket(AF_INET, SOCK_STREAM)                 #initialize client socket
    clientSocket.connect((serverName,serverPort))               #connect to xocket using incremented port number
    hello = 'ece2540 HELLO 001862203'                           #make and send greeting again to allow for a response to be waiting when function rejoins main
    clientSocket.send(hello.encode())                           

#function to evaluate the response from the list
def evaluate(serverresponselist):                               
    num1 = int(serverresponselist[2])                           #convert strings to integers
    num2 = int(serverresponselist[4])
    print(num1, num2)                                           
    operation = serverresponselist[3]                           #set variable to string of operation to be evaluated by if statemnts
    if operation == '+':                                        #if the string is an additor, add numbers
        answer = num1 + num2
    elif operation == '-':                                      #if string is minus sign, subtract num2 from num1
        answer = num1 - num2
    elif operation == '*':                                      #if multiplication, multiply numbers
        answer = num1 * num2
    elif operation == '/':                                      #if division, divide numbers
        answer = num1 / num2
    answer = str(answer)                                        #convert integer answer into string and return
    print(answer)
    return answer

#main function
def main():
    clientSocket.connect((serverName,serverPort))               #connect to server using initialized server IP and port
    hello = 'ece2540 HELLO 001862203'                           #set and encode greeting
    clientSocket.send(hello.encode())                           #send encoded greeting

    while 1:
        serverresponse = clientSocket.recv(1024)                #store server response in variable  
        serverresponse = serverresponse.decode()                #decoe response
        serverresponselist = serverresponse.split()             #split string to evaluate various elements of response
        print ('From Server:', serverresponselist)
        if len(serverresponse) == 0:                            #if the string is empty, the server has not returned a response and the next port will be tried
            print('EMPTY')
            nextport()                                          #call the next port function, which will make appropriate adjustments to connection and try again
        elif serverresponselist[1] == 'ERROR':                  #if the server returns an error, let user know
            print('ERROR')
        elif serverresponselist[1] == 'STATUS':                 #if the respose returns a status, the evaluation function will be called to evaluate said response
            answer = evaluate(serverresponselist)               #store answer to respose in variable
            clientSocket.send(answer.encode())                  #send encoded answer to server
        else:
            print ('BYE')                                       #the flag was obtained!
            clientSocket.close()                                #close connection (though server already has)
            break                                               #break the while loop

if __name__ == '__main__':
    main()                                                      #execute main funcitoin