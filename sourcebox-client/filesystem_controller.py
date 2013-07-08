# -*- coding: utf-8 -*-#
# Imports
import os
import logging
from threading import Timer
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

# @package Filesystem_Controller 
# Handles file-system-events
# @author Emu


# class Filesystem_Controller inherits from FileSystemEventHandler for overwriting event methods
class Filesystem_Controller(FileSystemEventHandler):

    # Variables
    lockTime = 5					# auto unlock after seconds: demo 20 seconds, final 5 min
    ignoreCreate = []				# list of paths whose fs-create-events shall be ignored
    ignoreDelete = []				# list of paths whose fs-delete-events shall be ignored
    ignoreMove = []					# list of paths whose fs-move-events shall be ignored
    ignoreModify = []				# list of paths whose fs-modify-events shall be ignored
    locked_files = []				# list of locked files		

    # Constuctor
    # @param client object of parent class
    # @param boxPath path to the directory that will be observed  
    # @author Emanuel Regnath
    def __init__(self, client, boxPath):
    	# catch logging object from sourceBox_client
        global log
       	log = logging.getLogger("client")

        self.boxPath = os.path.abspath(boxPath)						# absolute path of the observed directory (where fs-events will be detected)
        # os.chdir(boxPath)
        self.client = client										# object pointer to the parent class (client) 
        self.observer = Observer()									# create observer
        self.observer.schedule(self, boxPath, recursive=True)		# attach path to observer (recursive: also observe sub-directories)
        self.observer.start()										# start observing							
        log.info(
        	'Created Filesystem_Controller in path %s', boxPath)	# log

    # Destructor
    def __del__(self):
        log.info('Deleted Filesystem_Controller')					# log
        self.observer.stop()										# stop observing


    ## FS Control Methods (call from extern classes)
    #==========================================================================

    # locks a file
    # @param path path of the file relative to boxPath
    # @author Emanuel Regnath
    def lockFile(self, path):
        relpath = os.path.relpath(path, self.boxPath) 				# reduce to path relative to boxPath
        try:
            self.locked_files.append(relpath)							# new entry in locked_files

            self.ignoreModify.append(path)							# ignore modify-event raised by chmod
            path = os.path.join(self.boxPath, path)					# expand to absolute path
            os.chmod(path, 0o000)									# set file permissions: no read, no write, no exec
            print "File locked ", path 								# log
        except Exception, e:
        	log.error(
        		"could not lock file %s because %s", path, e)		# print exception

    # unlocks a file
    # @param path path of the file relative to boxPath
    # @author Emanuel Regnath
    def unlockFile(self, path):
        relpath = os.path.relpath(path, self.boxPath) 				# reduce to path relative to boxPath
        try:
            log.info('Unlocking ' + relpath)
            self.client.comm.send_unlock_file(relpath)				# send unlock command from client to server

            #self.locked_files.remove(relpath)							# remove file from locked list
            self.client.gui.locked_files.set(						# new entry in GUI notification
            	'\n'.join(self.locked_files))		

            self.ignoreModify.append(path)							# ignore modify-event triggered by chmod
            path = os.path.join(self.boxPath, path)					# expand to absolute path
            os.chmod(path, 0o666)									# set file permissions: read and write
            print "File unlocked: ", path
        except Exception, e:
        	log.error(
        		"could not unlock file %s because %s", path, e)		# print exception

    # wait a certain time (new thread) until path is auto-unlocked
    # @param path path of the file relative to boxPath
    # @param time time to wait in seconds
    # @author Emanuel Regnath
    def setLockTimer(self, path, time):
        Timer(time, self.unlockFile, (path,)).start()				# start new thread with timer

    # reads a file
    # @param path path of the file relative to boxPath
    # @author Emanuel Regnath
    # @returns the content of the file
    def readFile(self, path):
    	path = os.path.join(self.boxPath, path)						# expand to absolute path
        return open(path, 'r').read()

    # overwrites a file
    # @param path path of the file relative to boxPath
    # @param content content of the file   
    # @author Emanuel Regnath
    def writeFile(self, path, content):
        self.ignoreModify.append(path)								# ignore modify-event triggered by .write
        path = os.path.join(self.boxPath, path)						# expand to absolute path
        if os.access(path, os.W_OK):
        	open(path, 'w').write(content)							# write content to file
        else:
       		fileMod = os.stat(path).st_mode & 0777					# get fileMod
        	os.chmod(path, 0o666)									# set file permissions: read and write
        	open(path, 'w').write(content)							# write content to file
        	os.chmod(path, fileMod)
        

    # created File
    # @param path path of the file relative to boxPath
    # @author Emanuel Regnath 
    def createFile(self, path):
        self.ignoreCreate.append(path)								# ignore create-event triggered by .close
        path = os.path.join(self.boxPath, path)						# expand to absolute path
        open(path, 'a').close()										# create file

    # create Directory
    # @param path path of the directory relative to boxPath
    # @author Emanuel Regnath 
    def createDir(self, path):
        self.ignoreCreate.append(path)								# ignore create-event triggered by os.makedirs
        path = os.path.join(self.boxPath, path)						# expand to absolute path
        os.makedirs(path)											# create directory

    # delete File
    # @param path path of the file relative to boxPath
    # @author Emanuel Regnath 
    def deleteFile(self, path):
        self.ignoreDelete.append(path)								# ignore delete-event triggered by os.remove
        path = os.path.join(self.boxPath, path)						# expand to absolute path
        os.remove(path)												# delete file

    # delete directory
    # @param path path of the directory relative to boxPath
    # @author Emanuel Regnath 
    def deleteDir(self, path):
        self.ignoreDelete.append(path)								# ignore delete-event triggered by os.removedirs
        path = os.path.join(self.boxPath, path)						# expand to absolute path
        os.removedirs(path)											# delete directory

    # moves or renames a File OR Directory
    # @param srcPath old path of the file or directory relative to boxPath
    # @param dstPath new path of the file or directory relative to boxPath  
    # @author Emanuel Regnath 
    def moveFileDir(self, srcPath, dstPath):
        self.ignoreMove.append(srcPath)								# ignore move-event triggered by os.renames
        srcPath = os.path.join(self.boxPath, srcPath)				# expand to absolute path
        dstPath = os.path.join(self.boxPath, dstPath)				# expand to absolute path
        # TODO: test if dest is in lokal folder?					
        os.renames(srcPath, dstPath)								# move file or directory

    # returns Size of a file in byte
    # @param path path of the file
    # @author Emanuel Regnath
    # @returns the size of the file
    def getSize(self, path):
    	path = os.path.join(self.boxPath, path)						# expand to absolute path
        return os.path.getsize(path)




    ## Filesystem Events (triggered by observer)
    #==========================================================================

    # triggered if a file or directory was created
    # @param event object representing the file system event
    # @author Emanuel Regnath 
    def on_created(self, event):
        src_path = event.src_path									# abslolute path
        src_relpath = os.path.relpath(src_path, self.boxPath) 		# reduce to path relative to boxPath
        if src_path in self.ignoreCreate:
            self.ignoreCreate.remove(src_path)
        else:
            if event.is_directory == True:							# if event was triggered by a directory
                log.info("Directory created: %s", src_path)			# log
                # push changes to SVN
            else:
                log.info("File created: %s", src_path)				# log
                content = open(src_path).read()						# ERROR: src_path only filename
                self.client.comm.send_create_file(
                    src_relpath, len(content), content)


    # triggered if a file or directory was deleted
    # @param event object representing the file system event
    # @author Emanuel Regnath 
    def on_deleted(self, event):
        src_path = event.src_path									# abslolute path
        src_relpath = os.path.relpath(src_path, self.boxPath) 		# reduce to path relative to boxPath
        if src_path in self.ignoreDelete:
            self.ignoreDelete.remove(src_path)
        else:
            if event.is_directory == True:							# if event was triggered by a directory
                log.info("Directory deleted: %s", src_path)			# log
                # push changes to SVN
            else:
                log.info("File deleted: %s", src_path)				# log
                self.client.comm.send_delete_file(src_relpath)		# send delete_file to server


    # triggered if a file or directory was modified
    # @param event object representing the file system event
    # @author Emanuel Regnath 
    def on_modified(self, event):
        src_path = event.src_path									# abslolute path
        src_relpath = os.path.relpath(src_path, self.boxPath) 		# reduce to path relative to boxPath
        if src_path in self.ignoreModify:
            self.ignoreModify.remove(src_path)
        else:
            if event.is_directory == True:							# if event was triggered by a directory
                log.info("Directory modified: %s", src_path)		# log
                # push changes to SVN
            else:
                log.info("File modified: %s", src_relpath)				# log
                # lock file:
                self.client.comm.send_lock_file(src_relpath)
                self.locked_files.append(src_relpath)
                self.client.gui.locked_files.set(
                    '\n'.join(self.locked_files))

                self.setLockTimer(src_relpath, self.lockTime)		# start lockTimer for auto-unlock
                # push changes to SVN:
                content = self.readFile(src_path)					# read file content
                self.client.comm.send_modify_file(					# send modify_file to server
                    src_relpath, len(content), content)


    # triggered if a file or directory was moved or renamed
    # @param event object representing the file system event
    # @author Emanuel Regnath 
    def on_moved(self, event):
    	src_path = os.path.relpath(event.src_path, self.boxPath)	# reduce to path relative to boxPath
    	dest_path = os.path.relpath(event.dest_path, self.boxPath)	# reduce to path relative to boxPath	
        if src_path in self.ignoreMove:
            self.ignoreMove.remove(src_path)
        else:
            if event.is_directory == True:							# if event was triggered by a directory
                log.info("Directory moved from %s to %s", 
                	src_path, dest_path)							# log
                # push changes to SVN
            else:
                log.info("File moved from %s to %s", 
                	src_path, dest_path)							# log
                if src_path == None:
                    # same as create
                    pass
