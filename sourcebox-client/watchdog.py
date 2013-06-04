# coding: utf-8
'''-------------------------------------------------------------
' sourceboxclient – observe filesystem events  
' @encode: 	UTF-8, tabwidth = , newline = LF
' @date:	03.06.13
' @author: 	GRUPPE 4
'
'----------------------------------------------------------- ''' 
 




#################################################
#   		O W N    F U N C T I O N S			#
#################################################


def lockFile(file):
	print "File " + file + " locked!"



def updateFile(file):





#################################################
#  			M A I N   P R O G R A M				#
#################################################
from socket import *
import os, time
serverPort = 8080


# open client socket
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.settimeout(3.0)


# main loop:
while(1):

	# receive lock command from server


	# wait for files system events
