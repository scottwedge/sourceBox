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
    
    ## Is called when the client recieves a new file from the server
    #def get_new_file(self, path, content):
    #    pass

    ## Is called when a file on the server is deleted
    def get_delete_file(self, path):
        pass

    ## Is called when a file on the server is modified
    # @param path the path to the modified file
    # @param content a string containing the updated file content
    def get_modify_file(self, path, content):
        pass

    ## Sends a command to the server that creates an empty file
    # @author Paul
    # @param filePath of the new file related to sourceBox
    # @return 0 -1 -2 -3 
    def send_create_file(self, filePath, size, content):
        return self._SendCommand2(self.COMMAND_SENDCREATEFILE, filePath, size, content, 'filecreated')

    ## Sends the content of the file
    # @author Paul
    # @param path the path of the file
    # @param content the modified file content
    def send_modify_file(self, filePath, size, content):
        return self._SendCommand2(self.COMMAND_SENDMODIFYFILE, filePath, size, content, 'filemodified')


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
    # @return 0 -1 -3 
    def send_lock_file(self, filePath):
        return self._CommandSend(self.COMMAND_SENDLOCKFILE, filePath, 'filelocked')
    #
    def send_unlock_file(self, filePath):
        return self._CommandSend(self.COMMAND_SENDUNLOCKFILE, filePath, 'fileunlocked')

    def send_delete_file(self, filePath):
        return self._CommandSend(self.COMMAND_SENDDELETEFILE, filePath, 'filedeleted')

     
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
    # @param old_path old path of the file
    # @param new_path new path of the file
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


    ## Creates a dir
    # @author Paul
    # @param path the path of the dir
    def send_create_directory(self, path):
        pass



    # Internal functions
    def _create_socket(self):
        pass




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


    def GetVersion(sock):
        #for testing, returns the version of server
        sock.sendall(COMMAND_GETVERSION + ' ')
        ver = sock.recv(1024)   
        return ver 

    def GetFileSize(sock, fileName):
        #returns filesize from a file on server
        sock.sendall(COMMAND_GETFILESIZE + ' ' + fileName)
        resp = sock.recv(1024)
        size = int(resp)   
        return size 

    def GetFileSizeDirect(filePath):
        #returns filesize from a file on client pc
        if os.path.exists(filePath):
            return os.path.getsize(filePath)
        else:
            return -1


    def GetFile(sock, filePath):
        sock.sendall(COMMAND_GETFILE + ' ' + filePath)
        print "send command"
        r = sock.recv(2)
        print "recv ok"
        size = int(sock.recv(16))
        print "size", size
        recvd = ''
        while size > len(recvd):
            data = sock.recv(1024)
            if not data: 
                break
            recvd += data
        sock.sendall('ok')
        return recvd

    
    #print "Start client ..."
    #try:
        #filePathBase = os.path.dirname(__file__)

        #downloadDir = os.path.join(filePathBase, DOWNLOAD_DIR)
        #if not os.path.exists(downloadDir):
        #    os.makedirs(downloadDir)

        #actualSocket = _OpenServerSocket()
        #try:
            #fileName1 = 'text.txt'
            #fileName2 = 'text2.txt'        
            #recvfile1 = GetFile(actualSocket, fileName1)
            #filePath1 = os.path.join(downloadDir, fileName1)
            #with open(filePath1,"w") as f:
            #    f.write(recvfile1)
            #    f.close()

            #recvfile2 = GetFile(actualSocket, fileName2)
            #filePath2 = os.path.join(downloadDir, fileName2)
            #with open(filePath2,"w") as f:
            #    f.write(recvfile2)
            #    f.close()  
            #version = GetVersion(actualSocket)
            #print (version)
     
            #fileName = "tet.txt"
            #size = GetFileSize(actualSocket, fileName)
            #print fileName, size, "Bytes"

    #    except:
    #        print "Unexpected error:", sys.exc_info()[0]
    #        #raise     
    #    finally:
    #        _CloseServerSocket(actualSocket)
    
    #finally:
    #    _PressEnterKey()