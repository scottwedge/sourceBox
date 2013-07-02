# -*- coding: utf-8 -*-#
## sourceboxclient – Client_Communication_Controller
# handles the communication with the server
#
# @encode:  UTF-8, tabwidth = , newline = LF
# @author:  Paul

import socket,  sys, thread

class Client_Communication_Controller(object):
    
    # Client initiates the action and send a command to the server
    COMMAND_SENDCREATEFILE = 'SendCreateFile'
    COMMAND_SENDLOCKFILE = 'SendLockFile'
    COMMAND_SENDUNLOCKFILE = 'SendUnLockFile'
    COMMAND_SENDDELETEFILE = 'SendDeleteFile'
    COMMAND_SENDMODIFYFILE = 'SendModifyFile'
    COMMAND_SENDMOVEFILE = 'SendMoveFile'
    COMMAND_SENDCREATEDIR = 'SendCreateDir'

    ## Constructor
    def __init__(self, ip, port):
        print ' Client Created Communication_Controller'

        # Creates the instance variable sock. This is the socket communicating with the server
        self.sock = self._open_server_socket(ip, port)
        # Starts a thread listening for server events
        thread.start_new_thread(self._listen_for_sever_commands, (
            'Communication_Controller Thread for listening', self.sock))

    
    ## Deconstructor  
    def __del__(self):
        # Closes the socket when the instance is destructed
        self._close_socket(self.sock)
    

    ## Sends a command to the server that creates a file with content
    # @author Paul
    # @param filePath of the new file related to sourceBox, size, content
    # @return 0: True -1: False -2: Save problem on server -3: Sending problem 
    def send_create_file(self, filePath, size, content):
        return self._send_command(self.COMMAND_SENDCREATEFILE, filePath, size, content, 'filecreated')

    ## Sends a command to the server that modiry a file with new content
    # @author Paul
    # @param filePath of the new file related to sourceBox, size, content
    # @return 0: True -1: False -2: Save problem on server -3: Sending problem
    def send_modify_file(self, filePath, size, content):
        return self._send_command(self.COMMAND_SENDMODIFYFILE, filePath, size, content, 'filemodified')

    #call funktions with filePath
    def _command_send(self, command, filePath, returnMessage):
        mess = command + ' ' + filePath
        self.controller_socket.sendall(mess)
        ok = self.controller_socket.recv(2)
        if ok == 'ok':
            messLen = len(returnMessage) 
            answer = self.controller_socket.recv(messLen)
            if answer == returnMessage:
               return 0 #True
            else:
                return -1 #False
        return -3 # Sending problem

    #call funktions with filePath, content
    def _send_command(self, command, filePath, size, content, returnMessage):
        mess = command + ' ' + str(size) + ' ' + filePath
        self.controller_socket.sendall(mess)
        ok = self.controller_socket.recv(2)
        if ok == 'ok':
            self.controller_socket.sendall(content)
            contenttransferd = self.controller_socket.recv(2)
            if contenttransferd == 'ok':
                messLen = len(returnMessage)  
                answer = self.controller_socket.recv(messLen)
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
        return self._command_send(self.COMMAND_SENDLOCKFILE, filePath, 'filelocked')

    ## Sends a unlock command to the server
    # @author Paul
    # @param filePath of the new file related to sourceBox
    # @return 0: True -1: False -2: Save problem on server -3: Sending problem
    def send_unlock_file(self, filePath):
        return self._command_send(self.COMMAND_SENDUNLOCKFILE, filePath, 'fileunlocked')
    
    ## Sends a delete command to the server
    # @author Paul
    # @param filePath of the new file related to sourceBox
    # @return 0: True -1: False -2: Save problem on server -3: Sending problem
    def send_delete_file(self, filePath):
        return self._command_send(self.COMMAND_SENDDELETEFILE, filePath, 'filedeleted')

    ## Sends a create diractory command to the server
    # @author Paul
    # @param filePath of the new dir related to sourceBox
    # @return 0: True -1: False -2: Save problem on server -3: Sending problem
    def send_create_dir(self, filePath):
        return self._command_send(self.COMMAND_SENDCREATEDIR, filePath, 'dircreated')

    ## Sends a move file command to the server
    # @author Paul
    # @param old_path, newpath of the new file related to sourceBox
    # @return 0: True -1: False -2: Save problem on server -3: Sending problem
    def send_move_file(self, old_path, new_path):
        mess = self.COMMAND_SENDMOVEFILE + ' ' + old_path
        self.controller_socket.sendall(mess)
        ok = self.controller_socket.recv(2)
        if ok == 'ok':
            self.controller_socket.sendall(new_path)
            ok = self.controller_socket.recv(2)
            if ok == 'ok':
                returnMessage = 'filemoved'
                messLen = len(returnMessage) 
                answer = self.controller_socket.recv(messLen)
                if answer == returnMessage:
                   return 0 #True
                else:
                    return -1 #False
            return -3 # Sending problem
        return -3
          
    ## Opens a socket
    # @returns a socket
    def _openr_socket(self, ip, port):
        try:
            sock = socket.socket()
            sock.connect((ip, port))
            return sock
        except:
            print "OpenServerSocket error:", sys.exc_info()[0]

    ## Closes the socket
    def _close_socket(self, sock):
        sock.sendall('end' + " ")
        sock.close()

    def _listen_for_sever_commands(self, thread_name, open_socket):
            print '[' + thread_name + '] ' + 'Created thread: ' + thread_name

            while True:
                open_socket.recv(1024)