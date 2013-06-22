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
' 18.06.13: Watchdog hinzugefügt, muss installiert werden: pip install watchdog
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
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


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
## CREATE FILESYSTEM EVENT HANDLER
## --------------------------------------------------------------
class MyEventHandler(FileSystemEventHandler):
	def __init__(self, observer):
		self.observer = observer

	def on_created(self, event):
		if event.is_directory == True:
			print "Directory created: ",event.src_path
			# push changes to SVN			
		else:
			print "File created: ",event.src_path
			# push changes to SVN
        
	def on_deleted(self, event):
		if event.is_directory == True:
			print "Directory deleted: ",event.src_path
			# push changes to SVN			
		else:
			print "File deleted: ",event.src_path
			# push changes to SVN
		
	def on_modified(self, event):
		if event.is_directory == True:
			print "Directory modified: ",event.src_path
			# push changes to SVN			
		else:
			print "File modified: ",event.src_path
			# push changes to SVN

	def on_moved(self, event):			# also for renames!
		if event.is_directory == True:
			print "Directory moved from: ",event.src_path
			print "to: ",event.dest_path
			# push changes to SVN			
		else:
			print "File moved from: ",event.src_path
			print "to: ",event.dest_path



## --------------------------------------------------------------
## START WATCHDOG
## --------------------------------------------------------------
observer = Observer()   
fs_event_handler = MyEventHandler(observer)

observer.schedule(fs_event_handler, boxPath, recursive=True)
observer.start()



## --------------------------------------------------------------
## MAIN PROGRAM
## --------------------------------------------------------------
# main loop:
try:
	while True:
		# receive lock command from server
		# wait for files system events
		time.sleep(1)
# unexpected exit
except KeyboardInterrupt:
	observer.stop()

	

