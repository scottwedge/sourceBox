# -*- coding: utf-8 -*-#
# Imports
import os
from threading import Timer
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

# @package Filesystem_Controller 
# Handles file-system-events
# @author Emu


# class Filesystem_Controller inherits from FileSystemEventHandler for overwriting event methods
class Filesystem_Controller(FileSystemEventHandler):

    # Variables
    lockTime = 20					# auto unlock after seconds: demo 20 seconds, final 5 min
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
        self.boxPath = boxPath										# path of the observed directory (where fs-events will be detected)
        self.client = client										# object pointer to the parent class (client) 
        self.observer = Observer()									# create observer
        self.observer.schedule(self, boxPath, recursive=True)		# attach path to observer (recursive: also observe sub-directories)
        self.observer.start()										# start observing							
        print 'Created Filesystem_Controller in path: ' + boxPath	# log

    # Destructor
    def __del__(self):
        print 'Deleted Filesystem_Controller'						# log
        self.observer.stop()										# stop observing


    ## FS Control Methods (call from extern classes)
    #==========================================================================

    # locks a file
    # @param path path of the file
    # @author Emanuel Regnath
    def lockFile(self, path):
        try:
            file_name = os.path.basename(path)	
            self.locked_files.append(file_name)						# new entry in locked_files

            self.ignoreModify.append(path)							# ignore modify-event raised by chmod
            os.chmod(path, 0o000)									# set file permissions: no read, no write, no exec
            print "File locked ", path 								# log
        except Exception, e:
            print "Error: could not lock file ", path	
            print "because ", e										# print exception

    # unlocks a file
    # @param path path of the file
    # @author Emanuel Regnath
    def unlockFile(self, path):
        try:
            self.client.comm.send_unlock_file(path)					# send unlock command from client to server
            file_name = os.path.basename(path)
            self.locked_files.remove(file_name)						# remove file from locked list
            self.client.gui.locked_files.set(						# new entry in GUI notification
            	'\n'.join(self.locked_files))		

            self.ignoreModify.append(path)							# ignore modify-event triggered by chmod
            os.chmod(path, 0o666)									# set file permissions: read and write
            print "File unlocked: ", path
        except Exception, e:
            print "[ERROR] could not unlock file ", path
            print "because ", e

    # wait a certain time (new thread) until path is auto-unlocked
    # @param path path of the file
    # @param time time to wait in seconds
    # @author Emanuel Regnath
    def setLockTimer(self, path, time):
        Timer(time, self.unlockFile, (path,)).start()				# start new thread with timer

    # reads a file
    # @param path path of the file
    # @author Emanuel Regnath
    # @returns the content of the file
    def readFile(self, path):
        return open(path, 'r').read()

    # overwrites a file
    # @param path path of the file
    # @param content content of the file   
    # @author Emanuel Regnath
    def writeFile(self, path, content):
        self.ignoreModify.append(path)								# ignore modify-event triggered by .write
        open(path, 'w').write(content)								# write content to file

    # created File
    # @param path path of the file
    # @author Emanuel Regnath 
    def createFile(self, path):
        self.ignoreCreate.append(path)								# ignore create-event triggered by .close
        open(path, 'a').close()										# create file

    # create Directory
    # @param path path of the directory
    # @author Emanuel Regnath 
    def createDir(self, path):
        self.ignoreCreate.append(path)								# ignore create-event triggered by os.makedirs
        os.makedirs(path)											# create directory

    # delete File
    # @param path path of the file
    # @author Emanuel Regnath 
    def deleteFile(self, path):
        self.ignoreDelete.append(path)								# ignore delete-event triggered by os.remove
        os.remove(path)												# delete file

    # delete directory
    # @param path path of the directory
    # @author Emanuel Regnath 
    def deleteDir(self, path):
        self.ignoreDelete.append(path)								# ignore delete-event triggered by os.removedirs
        os.removedirs(path)											# delete directory

    # moves or renames a File OR Directory
    # @param srcPath old path of the file/directory
    # @param dstPath new path of the file/directory    
    # @author Emanuel Regnath 
    def moveFileDir(self, srcPath, dstPath):
        self.ignoreMove.append(srcPath)								# ignore move-event triggered by os.renames
        # TODO: test if dest is in lokal folder?					
        os.renames(srcPath, dstPath)								# move file or directory

    # returns Size of a file in byte
    # @param path path of the file
    # @author Emanuel Regnath
    # @returns the size of the file
    def getSize(self, path):
        return os.path.getsize(path)




    ## Filesystem Events (triggered by observer)
    #==========================================================================

    # triggered if a file or directory was created
    # @param event object representing the file system event
    # @author Emanuel Regnath 
    def on_created(self, event):
        if event.src_path in self.ignoreCreate:
            self.ignoreCreate.remove(event.src_path)
        else:
            if event.is_directory == True:							# if event was triggered by a directory
                print "Directory created: ", event.src_path
                # push changes to SVN
            else:
                print "File created: ", event.src_path
                file_name = os.path.basename(event.src_path)
                current_file = open(event.src_path)
                file_content = current_file.read()
                self.client.comm.send_create_file(
                    file_name, len(file_content), file_content)


    # triggered if a file or directory was deleted
    # @param event object representing the file system event
    # @author Emanuel Regnath 
    def on_deleted(self, event):
        if event.src_path in self.ignoreDelete:
            self.ignoreDelete.remove(event.src_path)
        else:
            if event.is_directory == True:							# if event was triggered by a directory
                print "Directory deleted: ", event.src_path
                #
            else:
                print "File deleted: ", event.src_path
                file_name = os.path.basename(event.src_path)
                self.client.comm.send_delete_file(file_name)		# send delete_file to server


    # triggered if a file or directory was modified
    # @param event object representing the file system event
    # @author Emanuel Regnath 
    def on_modified(self, event):
        if event.src_path in self.ignoreModify:
            self.ignoreModify.remove(event.src_path)
        else:
            if event.is_directory == True:							# if event was triggered by a directory
                print "Directory modified: ", event.src_path
                # push changes to SVN
            else:
                print "File modified: ", event.src_path				# log
                # lock file:
                file_name = os.path.basename(event.src_path)

                self.client.comm.send_lock_file(file_name)
                self.locked_files.append(file_name)
                self.client.gui.locked_files.set(
                    '\n'.join(self.locked_files))

                self.setLockTimer(file_name, self.lockTime)			# start lockTimer for auto-unlock
                # push changes to SVN:
                content = self.readFile(event.src_path)				# read file content
                self.client.comm.send_modify_file(					# send modify_file to server
                    file_name, len(content), content)


    # triggered if a file or directory was moved or renamed
    # @param event object representing the file system event
    # @author Emanuel Regnath 
    def on_moved(self, event):			
        if event.src_path in self.ignoreMove:
            self.ignoreMove.remove(event.src_path)
        else:
            if event.is_directory == True:							# if event was triggered by a directory
                print "Directory moved from: ", event.src_path
                print "to: ", event.dest_path
                # push changes to SVN
            else:
                print "File moved from: ", event.src_path
                print "to: ", event.dest_path
                if event.src_path == None:
                    # same as create
                    pass
