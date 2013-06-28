# -*- coding: utf-8 -*-#
# Imports
import os
from threading import Timer
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

## Handles file-system-events
# @author Emu
class Filesystem_Controller(FileSystemEventHandler):

	## Variables
	lockTime = 5		# 10 min
	ignoreEvent = 0


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
	def lockFile(self, path):
		try:
			os.chmod(path,0o000)
			self.ignoreEvent += 1		# prevent recognizing the lock ToDo: timer for ignore
			self.setLockTimer(path, self.lockTime)
			print "File locked ",path
		except Exception, e: 
			print "Error: could not lock file ",path
			print "because ", e

	def allOK(self):
		print "All OK"
	
	def unlockFile(self, path):
		try:
			os.chmod(path,0o666)
			self.ignoreEvent += 1		# prevent recognizing the lock
			print "File unlocked: ",path
		except Exception, e: 
			print "Error: could not unlock file ",path
			print "because ", e

	# wait lockTime until path is auto-unlocked
	def setLockTimer(self, path, time):
		t = Timer(time, self.unlockFile, (path,)).start()




	def readFile(self, path):
		return open(path, 'r').read()

	def writeFile(self, path, content):
		open(path, 'w').write(content)

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
			if self.ignoreEvent == 0:
				print "File modified: ",event.src_path
				# push changes to SVN
			else: self.ignoreEvent -= 1

	def on_moved(self, event):			# also for renames!
		if event.is_directory == True:
			print "Directory moved from: ",event.src_path
			print "to: ",event.dest_path
			# push changes to SVN			
		else:
			print "File moved from: ",event.src_path
			print "to: ",event.dest_path
