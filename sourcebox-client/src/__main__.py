#
# sourceboxclient – main
#
# @encode  UTF-8, tabwidth = , newline = LF
# @date   03.06.13
# @author  Johannes
#


'''-------------------------------------------------------------
' Planung/ToDo/Changelog:
'
' Wie können FS Events erkannt werden? ständiges überprüfen oder system calls fangen?
' 	pypi.python.org/pypi/watchdog
'
'
'
'----------------------------------------------------------- '''


from socket import *
import os
import time
serverPort = 8080

boxPath = "./" 			# path to the TumBox folder


# open client socket
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.settimeout(3.0)


# main loop:
while(1):

        # receive lock command from server


        # wait for files system events
