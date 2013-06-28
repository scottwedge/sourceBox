import communication_controller
import data_controller

# @package sourceboxServer
# the server
#
# @author  Kai and Martin
#
class SourceBoxServer(object):

    ## Creates a new instance of the SourceBoxServer
    def __init__(self):
        self.data = data_controller.Data_Controller('./data/')
        self.comm = communication_controller.Communication_Controller(self)
        
        # Just some random tests

        # data.create_file('test.txt')
        # self.data.lock_file('./data/test.txt')
        # self.data.save_file('./data/test.txt', 'Another test content')
        # print self.data.show_changes('./data/test.txt')
        # print self.data.read_file('./data/test.txt')
        
        print 'sourceBox server is running'
        #self.comm.unlock_file()
        self._command_loop()

    # When a new client connects
    # @returns a communication controller
    def new_client(self, computer_name):
        pass


    ## The server command loop
    def _command_loop(self):
        while True:
            pass

    ## Is called when a client creates a file.
    # Creates the file on all clients and in the data backend
    def create_file(self, path, name, content):
        self.data.create_file(file_name)
        # return true if successfully created
    
    ## Is called when a client locks a file.
    # Locks the file in the backend
    # @param file_name
    def lock_file(self, path, file_name):
        self.data.lock_file(file_name)
        # return true if successfully locked

    ## Is called when a client unlocks a file.
    # Unlocks the file in the backend
    # @param file_name
    def unlock_file(self, path, name):
        self.data.unlock_file(file_name)
        # return true if successfully unlocked

    ## Is called when a client changes a file.
    # Updates the file on all clients and in the data backend
    def modify_file(self, path, name, content):
        # return true if successfully modified
        pass

    ## Is called when a client deletes a file.
    # Deletes the file on all clients and in the data backend
    def delete_file(self, path, name):
        # return true if successfully deleted
        pass
