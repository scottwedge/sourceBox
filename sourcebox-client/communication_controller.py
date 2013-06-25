# -*- coding: utf-8 -*-#
## sourceboxclient – communication_controller
# handles the communication with the server
#
# @encode:  UTF-8, tabwidth = , newline = LF
# @author:  Paul


class Communication_Controller(object):

    import socket, time, sys, os

    COMMAND_GETVERSION = 'GetVersion'
    COMMAND_GETFILESIZE = 'GetFileSize'
    COMMAND_GETFILE = 'GetFile'
    DOWNLOAD_DIR = 'Download'

    ## Constructor
    def __init__(self):
        #open client TCP-Socket
        #from socket import *
        #clientSocket = socket(AF_INET, SOCK_STREAM)
        #clientSocket.settimeout(3.0)
        actualSocket = _OpenServerSocket()
        print ' Client Created Communication_Controller'
    
    ## Deconstructor  
    def __del__(self):
        #close client socket
        #clientSocket.close
        _CloseServerSocket(actualSocket)
        pass
    
    ## Is called when the client recieves a new file from the server
    def get_new_file(self, path, content):
        pass

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
    # @param path the path of the new file
    def send_create_file(self, path):
        pass

    ## Sends a lock command to the server
    # @author Paul
    # @param path the path to the file
    # @returns true/false
    def send_lock_file(self, path):
        pass

    ## Sends the content of the file
    # @author Paul
    # @param path the path of the file
    # @param content the modified file content
    def send_modify_file(self, path, content):
        pass

    ## Unlocks a file
    # @author Paul
    # @param path the path of the file
    def send_unlock_file(self, path):
        pass

    ## Deletes a file
    # @author Paul
    # @param path the path of the file
    def send_delete_file(self, path):
        pass

    ## Sends a move file command to the server
    # @author Paul
    # @param old_path old path of the file
    # @param new_path new path of the file
    def send_move_file(self, old_path, new_path):
        pass

    ## Creates a dir
    # @author Paul
    # @param path the path of the dir
    def send_create_directory(self, path):
        pass

    # Internal functions
    def _create_socket():
        pass




    def _PressEnterKey():
        print "Please, Press Enter Key ..."
        data = sys.stdin.readline()
        return 0

    def _OpenServerSocket():
        sock = socket.socket()
        sock.connect(('192.168.1.34', 50000))
        return sock

    def _CloseServerSocket(sock):
        sock.sendall('end' + " ")
        sock.close()


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