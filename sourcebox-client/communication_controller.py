# -*- coding: utf-8 -*-#
## sourceboxclient – communication_controller
# handles the communication with the server
#
# @encode:  UTF-8, tabwidth = , newline = LF
# @author:  Paul


class Communication_Controller(object):

    ## Constructor
    def __init__(self):
        #open client TCP-Socket
        #from socket import *
        #clientSocket = socket(AF_INET, SOCK_STREAM)
        #clientSocket.settimeout(3.0)
        print 'Created Communication_Controller'
    
    ## Deconstructor  
    def __del__(self):
        #close client socket
        #clientSocket.close
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
