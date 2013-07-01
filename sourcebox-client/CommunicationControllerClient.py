# -*- coding: utf-8 -*-#
## sourceboxclient – communication_controller
# handles the communication with the server
#
# @encode:  UTF-8, tabwidth = , newline = LF
# @author:  Paul

import socket, time, sys, os

class CommunicationControllerClient(object):
    
    # Client initiates the action and send a command to the server
    COMMAND_SENDCREATEFILE = 'SendCreateFile'
    COMMAND_SENDLOCKFILE = 'SendLockFile'
    COMMAND_SENDUNLOCKFILE = 'SendUnLockFile'
    COMMAND_SENDDELETEFILE = 'SendDeleteFile'
    COMMAND_SENDMODIFYFILE = 'SendModifyFile'
    COMMAND_SENDMOVEFILE = 'SendMoveFile'
    COMMAND_SENDCREATEDIR = 'SendCreateDir'

    ## Constructor
    def __init__(self, parent):
        self.parent = parent
        print ' Client Created Communication_Controller'
    
    ## Deconstructor  
    def __del__(self):
        #close client socket
        #clientSocket.close
        #_CloseServerSocket(actualSocket)
        pass
    

    ## Sends a command to the server that creates a file with content
    # @author Paul
    # @param filePath of the new file related to sourceBox, size, content
    # @return 0: True -1: False -2: Save problem on server -3: Sending problem 
    def send_create_file(self, filePath, size, content):
        return self._SendCommand2(self.COMMAND_SENDCREATEFILE, filePath, size, content, 'filecreated')

    ## Sends a command to the server that modiry a file with new content
    # @author Paul
    # @param filePath of the new file related to sourceBox, size, content
    # @return 0: True -1: False -2: Save problem on server -3: Sending problem
    def send_modify_file(self, filePath, size, content):
        return self._SendCommand2(self.COMMAND_SENDMODIFYFILE, filePath, size, content, 'filemodified')

    #call funktions with filePath, content
    def _SendCommand2(self, command, filePath, size, content, returnMessage):
        mess = command + ' ' + str(size) + ' ' + filePath
        self.ControllerSocket.sendall(mess)
        ok = self.ControllerSocket.recv(2)
        if ok == 'ok':
            self.ControllerSocket.sendall(content)
            contenttransferd = self.ControllerSocket.recv(2)
            if contenttransferd == 'ok':
                messLen = len(returnMessage)  
                answer = self.ControllerSocket.recv(messLen)
                if answer == returnMessage:
                    return 0 #True
                else:
                    return -1 #False
            return -2 # Content save problem
        else:
            return -3 # Sending problem

    ## Sends a lock command to the server
    # @author Paul
    # @param filePath of the new file related to sourceBox
    # @return 0: True -1: False -2: Save problem on server -3: Sending problem
    def send_lock_file(self, filePath):
        return self._CommandSend(self.COMMAND_SENDLOCKFILE, filePath, 'filelocked')

    ## Sends a unlock command to the server
    # @author Paul
    # @param filePath of the new file related to sourceBox
    # @return 0: True -1: False -2: Save problem on server -3: Sending problem
    def send_unlock_file(self, filePath):
        return self._CommandSend(self.COMMAND_SENDUNLOCKFILE, filePath, 'fileunlocked')
    
    ## Sends a delete command to the server
    # @author Paul
    # @param filePath of the new file related to sourceBox
    # @return 0: True -1: False -2: Save problem on server -3: Sending problem
    def send_delete_file(self, filePath):
        return self._CommandSend(self.COMMAND_SENDDELETEFILE, filePath, 'filedeleted')

    ## Sends a create diractory command to the server
    # @author Paul
    # @param filePath of the new dir related to sourceBox
    # @return 0: True -1: False -2: Save problem on server -3: Sending problem
    def send_create_dir(self, filePath):
        return self._CommandSend(self.COMMAND_SENDCREATEDIR, filePath, 'dircreated')
     
    #call funktions with filePath
    def _CommandSend(self, command, filePath, returnMessage):
        mess = command + ' ' + filePath
        self.ControllerSocket.sendall(mess)
        ok = self.ControllerSocket.recv(2)
        if ok == 'ok':
            messLen = len(returnMessage) 
            answer = self.ControllerSocket.recv(messLen)
            if answer == returnMessage:
               return 0 #True
            else:
                return -1 #False
        return -3 # Sending problem


    ## Sends a move file command to the server
    # @author Paul
    # @param old_path, newpath of the new file related to sourceBox
    # @return 0: True -1: False -2: Save problem on server -3: Sending problem
    def send_move_file(self, old_path, new_path):
        mess = self.COMMAND_SENDMOVEFILE + ' ' + old_path
        self.ControllerSocket.sendall(mess)
        ok = self.ControllerSocket.recv(2)
        if ok == 'ok':
            self.ControllerSocket.sendall(new_path)
            ok = self.ControllerSocket.recv(2)
            if ok == 'ok':
                returnMessage = 'filemoved'
                messLen = len(returnMessage) 
                answer = self.ControllerSocket.recv(messLen)
                if answer == returnMessage:
                   return 0 #True
                else:
                    return -1 #False
            return -3 # Sending problem
        return -3




    def _PressEnterKey(self):
        print "Please, Press Enter Key ..."
        data = sys.stdin.readline()
        return 0

    #
    def Init(self, strIP, intPORT):
      self.sIP = strIP
      self.iPORT = intPORT
      self.ControllerSocket = self._OpenServerSocket(strIP, intPORT)
    
    #
    def _OpenServerSocket(self, strIP, strPORT):
        try:
            sock = socket.socket()
            sock.connect((strIP, strPORT))
            return sock
        except:
            print "OpenServerSocket error:", sys.exc_info()[0]
            raise


    #def _CloseServerSocket(sock):
    #    sock.sendall('end' + " ")
    #    sock.close()


    #def GetVersion(sock):
    #    #for testing, returns the version of server
    #    sock.sendall(COMMAND_GETVERSION + ' ')
    #    ver = sock.recv(1024)   
    #    return ver 

    #def GetFileSize(sock, fileName):
    #    #returns filesize from a file on server
    #    sock.sendall(COMMAND_GETFILESIZE + ' ' + fileName)
    #    resp = sock.recv(1024)
    #    size = int(resp)   
    #    return size 

    #def GetFileSizeDirect(filePath):
    #    #returns filesize from a file on client pc
    #    if os.path.exists(filePath):
    #        return os.path.getsize(filePath)
    #    else:
    #        return -1


   