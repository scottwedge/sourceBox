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
        data = data_controller.Data_Controller('./data/')
        comm = communication_controller.Communication_Controller(self)
        
        # Just some random tests

        #data.create_file('test.txt')
        data.lock_file('./data/test.txt')
        data.save_file('./data/test.txt', 'Another test content')
        print data.show_changes('./data/test.txt')
        print data.read_file('./data/test.txt')
        print 'sourceBox server is running'
        
        self._command_loop()

    ## The server command loop
    def _command_loop(self):
        while True:
            pass

    def test(self):
        print 'test success'