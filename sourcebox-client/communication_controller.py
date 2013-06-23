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

    def update_files():
        pass

    # push functions (request)
    def create_file():
        pass

    def lock_file():
        pass

    def modify_file():
        pass

    def unlock_file():
        pass

    def delete_file():
        pass

    # Internal functions
    def _create_socket():
        pass
