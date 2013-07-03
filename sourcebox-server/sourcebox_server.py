import server_communication_controller
import data_controller
import os.path
import socket

# @package sourceboxServer
# the server
#
# @author  Kai and Martin
#


class SourceBoxServer(object):

    # Creates a new instance of the SourceBoxServer
    def __init__(self):
        try:
            self.data = data_controller.Data_Controller('./data/')

            # Contains all active Communication Controllers
            self.active_clients = []

            self.create_incoming_socket()
            # Just some random tests

            # data.create_file('test.txt')
            # self.data.lock_file('./data/test.txt')
                # self.data.save_file('./data/test.txt', 'Another test content')
            # print self.data.show_changes('./data/test.txt')
            # print self.data.read_file('./data/test.txt')

            print 'sourceBox server is running'
            # self.comm.unlock_file()
            self._command_loop( self.sock)
    

        # unexpected exit
        except KeyboardInterrupt:
            self.sock.close()
            del self.data
            for comm in self.active_clients:
                del comm
            print 'Terminating SourceBoxServer'


    # 
    def create_incoming_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('', 50000))
        self.sock.listen(5) # Max 5 Clients

    # When a new client connects
    # @returns a communication controller
    def new_client(self, connection):
        init_message = connection.recv(20).split(' ')
        if not init_message[0] == 'INIT':
            print '[WARNING] Init failed'
        else:
            computer_name = init_message[1]
            print 'A new client (' + computer_name + ')logged in. Creating a Communication Controller'

            comm = server_communication_controller.Server_Communication_Controller(self, connection, computer_name)
            
            self.active_clients.append(comm)
            print 'Active Clients are:'
            for client in self.active_clients:
                print client.computer_name

    def remove_client(self, client):
        print 'Remove client ' + client.computer_name

    # The server command loop
    def _command_loop(self, sock):
        while True:
            (connection, address) = sock.accept()
            self.new_client(connection)

    # Is called when a client creates a file.
    # Creates the file on all clients and in the data backend
    def create_file(self, path, file_name, content, computer_name):
        print 'Creating the file ' + file_name
        self.data.create_file(os.path.join(path, file_name), content)
        for comm in self.active_clients:
            if not comm.computer_name == computer_name: comm.send_create_file(100, file_name)
        # return true if successfully created
        return True

    # Is called when a client locks a file.
    # Locks the file in the backend
    # @param file_name
    def lock_file(self, path, file_name):
        self.data.lock_file(os.path.join(path, file_name))
        # return true if successfully locked
        return True

    # Is called when a client unlocks a file.
    # Unlocks the file in the backend
    # @param file_name
    def unlock_file(self, path, file_name):
        self.data.unlock_file(os.path.join(path, file_name))
        # return true if successfully unlocked
        return True

    # Is called when a client changes a file.
    # Updates the file on all clients and in the data backend
    def modify_file(self, path, file_name, content):
        # return true if successfully modified
        self.data.modify_file(file_name, content)
        return True

    # Is called when a client deletes a file.
    # Deletes the file on all clients and in the data backend
    def delete_file(self, path, file_name):
        # return true if successfully deleted
        self.data.delete_file(file_name)
        return True

    def get_file_size(self, path, file_name):
        if os.path.exists(os.path.join(path, file_name)):
            return os.path.getsize(os.path.join(path, file_name))
        else:
            return False
