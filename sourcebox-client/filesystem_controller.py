# -*- coding: utf-8 -*-#
# Imports
import os
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

## Handles file-system-events
# @author Emu
class Filesystem_Controller(FileSystemEventHandler):

	## Constuctor
	def __init__(self, boxPath):
		print 'Created Filesystem_Controller in path: ' + boxPath
		self.observer = Observer()
		self.observer.schedule(self, boxPath, recursive=True)
		self.observer.start()

	## Deconstructor
	def __del__(self):
		print 'Deleted Filesystem_Controller'
		self.observer.stop()


	## Controls
	#######################################################
	def lockFile(path):
		try:
			os.chmod(path,0o000)
			print "File locked: ",path
		except Exception: 
			print "Error: could not lock file ",path

	
	def unlockFile(path):
		try:
			os.chmod(path,0o666)
			print "File unlocked: ",path
		except Exception: 
			print "Error: could not unlock file ",path



	## Events
	#######################################################
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
