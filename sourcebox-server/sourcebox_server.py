import communication_controller
import data_controller

# @package sourceboxServer
# the server
#
# @author  Kai
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

    ## The server command loop
    def _command_loop(self):
        while True:
            pass

    def test(self):
        print 'test success'

# Kais erste Gehversuche :)

    def update_file(self):
        pass

    def create_file(self, file_name):
        self.data.create_file(file_name)

    def lock_file(self, file_name):
        self.data.lock_file(file_name)

    def modify_file(self):
        pass

    def unlock_file(self, file_name):
        self.data.unlock_file(file_name)

    def delete_file(self):
        pass
