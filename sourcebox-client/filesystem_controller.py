# -*- coding: utf-8 -*-#
# Imports
import os
from threading import Timer
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

# Handles file-system-events
# @author Emu


class Filesystem_Controller(FileSystemEventHandler):

    # Variables
    lockTime = 5		# 10 min
    ignoreCreate = []
    ignoreDelete = []
    ignoreMove = []
    ignoreModify = []

    # Constuctor
    def __init__(self, client, boxPath):
        self.boxPath = boxPath
        self.client = client
        self.observer = Observer()
        self.observer.schedule(self, boxPath, recursive=True)
        self.observer.start()
        self.locked_files = []
        print 'Created Filesystem_Controller in path: ' + boxPath

    # Deconstructor
    def __del__(self):
        print 'Deleted Filesystem_Controller'
        self.observer.stop()

    # Controls (call from extern classes)
    #
    # locks a file
    def lockFile(self, path):
        try:
            file_name = os.path.basename(path)
            self.locked_files.append(file_name)

            os.chmod(path, 0o000)
            self.ignoreEvent += 1		# prevent recognizing the lock ToDo: timer for ignore
            print "File locked ", path
        except Exception, e:
            print "Error: could not lock file ", path
            print "because ", e

    # unlocks a file
    def unlockFile(self, path):
        try:
            self.client.comm.send_unlock_file(path)
            file_name = os.path.basename(path)
            self.locked_files.remove(file_name)
            self.client.gui.locked_files.set('\n'.join(self.locked_files))

            # os.chmod(path, 0o666)
            # self.ignoreEvent += 1		# prevent recognizing the lock
            print "File unlocked: ", path
        except Exception, e:
            print "Error: could not unlock file ", path
            print "because ", e

    # wait lockTime until path is auto-unlocked
    def setLockTimer(self, path, time):
        Timer(time, self.unlockFile, (path,)).start()

    # reads a file
    def readFile(self, path):
        return open(path, 'r').read()

    # overwrites a file
    def writeFile(self, path, content):
        self.ignoreModify.append(path)
        open(path, 'w').write(content)

    # create File
    def createFile(self, path):
        self.ignoreCreate.append(path)
        open(path, 'a').close()

    # create Directory
    def createDir(self, path):
        self.ignoreCreate.append(path)
        os.makedirs(path)

    # delete File
    def deleteFile(self, path):
        self.ignoreDelete.append(path)
        os.remove(path)

    # delete Directory
    def deleteDir(self, path):
        self.ignoreDelete.append(path)
        os.removedirs(path)

    # moves or renames a File OR Directory
    def moveFileDir(self, srcPath, dstPath):
        self.ignoreMove.append(srcPath)
        # test if dest is in lokal folder?
        os.renames(srcPath, dstPath)

    # return Size of path in byte
    def getSize(self, path):
        return os.path.getsize(path)

    # Filesystem Events
    #
    def on_created(self, event):
        if event.src_path in self.ignoreCreate:
            self.ignoreCreate.remove(event.src_path)
        else:
            if event.is_directory == True:
                print "Directory created: ", event.src_path
                # push changes to SVN
            else:
                print "File created: ", event.src_path
                file_name = os.path.basename(event.src_path)
                current_file = open(event.src_path)
                file_content = current_file.read()
                self.client.comm.send_create_file(
                    file_name, len(file_content), file_content)

    def on_deleted(self, event):
        if event.src_path in self.ignoreDelete:
            self.ignoreDelete.remove(event.src_path)
        else:
            if event.is_directory == True:
                print "Directory deleted: ", event.src_path
                #
            else:
                print "File deleted: ", event.src_path
                file_name = os.path.basename(event.src_path)
                self.client.comm.send_delete_file(file_name)

    def on_modified(self, event):
        if event.src_path in self.ignoreModify:
            self.ignoreModify.remove(event.src_path)
        else:
            if event.is_directory == True:
                print "Directory modified: ", event.src_path
                # push changes to SVN
            else:
                print "File modified: ", event.src_path
                # lock file:
                file_name = os.path.basename(event.src_path)

                self.client.comm.send_lock_file(file_name)
                self.locked_files.append(file_name)
                self.client.gui.locked_files.set(
                    '\n'.join(self.locked_files))

                self.setLockTimer(file_name, self.lockTime)
                # push changes to SVN:
                content = self.readFile(event.src_path)
                self.client.comm.send_modify_file(
                    file_name, len(content), content)

    def on_moved(self, event):			# also for renames!
        if event.src_path in self.ignoreMove:
            self.ignoreMove.remove(event.src_path)
        else:
            if event.is_directory == True:
                print "Directory moved from: ", event.src_path
                print "to: ", event.dest_path
                # push changes to SVN
            else:
                print "File moved from: ", event.src_path
                print "to: ", event.dest_path
                if event.src_path == None:
                    # same as create
                    pass
