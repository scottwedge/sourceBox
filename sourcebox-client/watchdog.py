# coding: utf-8
'''-------------------------------------------------------------
' sourceboxclient – observe filesystem events  
' @encode: 	UTF-8, tabwidth = , newline = LF
' @date:	03.06.13
' @author: 	GRUPPE 4 – Emanuel, wer noch?
'
'----------------------------------------------------------- ''' 
 
 
 '''-------------------------------------------------------------
' Planung/ToDo/Changelog:
'
' Wie können FS Events erkannt werden? ständiges überprüfen oder system calls fangen?
' 	pypi.python.org/pypi/watchdog
'	
'
'
'----------------------------------------------------------- ''' 




#################################################################
#   		O W N    F U N C T I O N S							#
#################################################################

def checkFiles(path):




def lockFile(file):
	print "File " + file + " locked!"



def updateFile(file):





#################################################################
#  			M A I N   P R O G R A M								#
#################################################################
from socket import *
import os, time
serverPort = 8080		

boxPath = "./" 			# path to the TumBox folder


# open client socket
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.settimeout(3.0)


# main loop:
while(1):

	# receive lock command from server


	# wait for files system events
