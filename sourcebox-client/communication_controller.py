'''-------------------------------------------------------------
' sourceboxclient – communication_controller
' handles the communication with the server
'
' @encode:  UTF-8, tabwidth = , newline = LF
' @date:    03.06.13
' @author:  GRUPPE 4 – Emanuel, wer noch?
'
'----------------------------------------------------------- '''


# push functions (requests)
class Communication_Controller(object):

    def __init__(self):
        #open client TCP-Socket
        from socket import *
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.settimeout(3.0)
        print 'Created Communication_Controller'
        
    def __del__(self):
        #close client socket
        clientSocket.close

    #
    def get_new_file(self, path, content):
        pass

    def get_delete_file(self, path):
        pass

    def get_modify_file(self, path, content):
        pass

    # push functions (request)
    # Sends a command to the server that creates an empty file
    def send_create_file(self, path):
        pass

    ## Sends a lock command to the server
    #  @returns true/false
    def send_lock_file(self, path):
        pass

    ## Sends the content of the file
    def send_modify_file(self, path, content):
        pass

    ## Unlocks a file
    def send_unlock_file(self, path):
        pass

    ## Deletes a file
    def send_delete_file(self, path):
        pass

    def send_move_file(self, old_path, new_path):
        pass


    def send_create_directory(self, path):
        pass

    # Internal functions
    def _create_socket():
        pass
