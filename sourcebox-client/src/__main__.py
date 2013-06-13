# -*- coding: utf-8 -*-#
# sourceboxclient – main
#
# @encode  UTF-8, tabwidth = 4 , newline = LF
# @date   03.06.13
# @author  Johannes
#


'''-------------------------------------------------------------
' Planung/ToDo/Changelog:
'
' 13.06.13: Funktionalitaet zum parsen der Configdatei hinzugefügt
'
'
'----------------------------------------------------------- '''


## --------------------------------------------------------------
## IMPORT SECTION
## --------------------------------------------------------------
from socket import *
import os
import time
import ConfigParser


## --------------------------------------------------------------
## PARSE CONFIG FILE
## --------------------------------------------------------------
config = ConfigParser.ConfigParser()
try:
	config.read("./sb_client.conf")
except:
	print "Error while trying to read config file. Check if 'sb_client.conf' exists in the same folder as the program file."

boxPath = config.get('main', 'path')

serverHostname = config.get('server', 'host')
serverPort = config.get('server', 'port')

username = config.get('user', 'name')
password = config.get('user', 'password')


## --------------------------------------------------------------
## OPEN CLIENT SOCKET
## --------------------------------------------------------------
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.settimeout(3.0)


## --------------------------------------------------------------
## MAIN PROGRAM
## --------------------------------------------------------------
# main loop:
while(1):
	
# receive lock command from server
	
# wait for files system events
	pass