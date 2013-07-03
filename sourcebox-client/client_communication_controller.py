# -*- coding: utf-8 -*-#
## sourceboxclient – Client_Communication_Controller
# handles the communication with the server
#
# @encode:  UTF-8, tabwidth = , newline = LF
# @author:  Paul

import socket,  threading

class Client_Communication_Controller(object):
    
    # Client initiates the action and send a command to the server
    COMMAND_SENDCREATEFILE = 'CREATE_FILE'
    COMMAND_SENDLOCKFILE = 'LOCK'
    COMMAND_SENDUNLOCKFILE = 'UNLOCK'
    COMMAND_SENDDELETEFILE = 'REMOVE'
    COMMAND_SENDMODIFYFILE = 'MODIFY'
    COMMAND_SENDMOVEFILE = 'MOVE'
    COMMAND_SENDCREATEDIR = 'CREATE_DIR'
    COMMAND_INIT = 'INIT'
    COMMAND_ACK = "OK\n"

    ## Constructor
    def __init__(self, ip, port, computer_name):
        print ' Client Created Communication_Controller'

        self.computer_name = computer_name

        # Creates the instance variable sock. This is the socket communicating with the server
        self.controller_socket = self._open_socket(ip, port)

        # Inits the connection
        self._init_connection()

        # Starts a thread listening for server events
        threading_queue = []
        self.command_listener_thread = Command_Recieve_Handler('Communication_Controller Thread for listening', self.controller_socket) 
        self.command_listener_thread.daemon = True 

        threading_queue.append(self.command_listener_thread) 
        self.command_listener_thread.start()
       
    
    ## Deconstructor  
    def __del__(self):
        # Closes the socket when the instance is destructed
        self._close_socket(self.sock)

    ## Initialises the connection
    def _init_connection(self):
        self.controller_socket.send(self.COMMAND_INIT + ' ' + self.computer_name)

    ## Sends a command to the server that creates a file with content
    # @author Paul
    # @param filePath of the new file related to sourceBox, size, content
    # @return 0: True -1: False -2: Save problem on server -3: Sending problem 
    def send_create_file(self, filePath, size, content):
        return self._send_command_with_content(self.COMMAND_SENDCREATEFILE, filePath, size, content)

    ## Sends a command to the server that modiry a file with new content
    # @author Paul
    # @param filePath of the new file related to sourceBox, size, content
    # @return 0: True -1: False -2: Save problem on server -3: Sending problem
    def send_modify_file(self, filePath, size, content):
        return self._send_command_with_content(self.COMMAND_SENDMODIFYFILE, filePath, size, content)

    ## Sends a command to the server (without content)
    # @throws IOError if a timeout occurs
    # @author Martin Zellner
    # @param command the command
    # @param file_path path to the file
    def _send_command(self, command, file_path):
        mess = command + ' ' + file_path
        self.controller_socket.send(mess)

        # Wait for the recieve thread to send us a ok Event
        status = self.command_listener_thread.ok.wait(5.0)
        self.command_listener_thread.ok.clear()
        if not status: raise IOError('Did not recieve a response from the server.')
        return True

    ## Sends a command to the server (with content)
    # @throws IOError if a timeout occurs
    # @author Martin Zellner
    # @param command the command
    # @param file_path path to the file
    # @param content the content of the file
    def _send_command_with_content(self, command, filePath, size, content):
        mess = command + ' ' + str(size) + ' ' + filePath
        self.controller_socket.sendall(mess)
        
        # Wait for the recieve thread to send us a ok Event
        status = self.command_listener_thread.ok.wait(5.0)
        self.command_listener_thread.ok.clear()
        if not status: raise IOError('Did not recieve a response from the server.')

        # Send the content
        self.controller_socket.send(content)

        # Wait for the recieve thread to send us a ok Event
        status = self.command_listener_thread.ok.wait(5.0)
        self.command_listener_thread.ok.clear()
        if not status: raise IOError('Did not recieve a response from the server.')

        return True

    ## Sends a lock command to the server
    # @author Paul
    # @param filePath of the new file related to sourceBox
    # @return 0: True -1: False -2: Save problem on server -3: Sending problem
    def send_lock_file(self, filePath):
        return self._send_command(self.COMMAND_SENDLOCKFILE, filePath)

    ## Sends a unlock command to the server
    # @author Paul
    # @param filePath of the new file related to sourceBox
    # @return 0: True -1: False -2: Save problem on server -3: Sending problem
    def send_unlock_file(self, filePath):
        return self._send_command(self.COMMAND_SENDUNLOCKFILE, filePath)
    
    ## Sends a delete command to the server
    # @author Paul
    # @param filePath of the new file related to sourceBox
    # @return 0: True -1: False -2: Save problem on server -3: Sending problem
    def send_delete_file(self, filePath):
        return self._send_command(self.COMMAND_SENDDELETEFILE, filePath)

    ## Sends a create diractory command to the server
    # @author Paul
    # @param filePath of the new dir related to sourceBox
    # @return 0: True -1: False -2: Save problem on server -3: Sending problem
    def send_create_dir(self, filePath):
        return self._send_command(self.COMMAND_SENDCREATEDIR, filePath)

    ## Sends a move file command to the server
    # @author Martin
    # @param old_path, newpath of the new file related to sourceBox
    # @return True
    # @throws IOError if a timeout occurs
    def send_move_file(self, old_path, new_path):
        mess = self.COMMAND_SENDMOVEFILE + ' ' + old_path
        self.controller_socket.sendall(mess)
        
        # Wait for the recieve thread to send us a ok Event
        status = self.command_listener_thread.ok.wait(5.0)
        self.command_listener_thread.ok.clear()
        if not status: raise IOError('Did not recieve a response from the server.')

        self.controller_socket.sendall(new_path)

        # Wait for the recieve thread to send us a ok Event
        status = self.command_listener_thread.ok.wait(5.0)
        self.command_listener_thread.ok.clear()
        if not status: raise IOError('Did not recieve a response from the server.')

        return True

    ## Opens a socket
    # @returns a socket
    def _open_socket(self, ip, port):
        try:
            sock = socket.socket()
            sock.connect((ip, port))
            return sock
        except IOError, e:
            raise e

    ## Closes the socket
    # @param sock the socket to close
    def _close_socket(self, sock):
        sock.sendall('end' + " ")
        sock.close()

class Command_Recieve_Handler(threading.Thread):
    COMMAND_ACK = "OK\n"
    COMMAND_CREATE = "CREATE"

    def __init__(self, thread_name, open_socket):
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.open_socket = open_socket
        self.ok = threading.Event()

    def run(self):
        print '[' + self.thread_name + '] ' + 'Created'
        while True:
            data = self.open_socket.recv(1024).split(' ')
            if data[0] == self.COMMAND_ACK: # If a OK was recieved
                # Send the OK Event
                self.ok.set()
            elif data[0] == self.COMMAND_CREATE:
                print 'Recieved Create Command' + data
                self.open_socket.send('OK\n')
            else:
                print 'Command recieved' + data