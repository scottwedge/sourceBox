#
# sourceboxServer – main
# handles the communication with the server
#
# @encode  UTF-8, tabwidth = , newline = LF
# @author  Kai
#


import communication_controller
import data_controller


class SourceBoxServer(object):

    def __init__(self):
        data = data_controller.Data_Controller('./data/')
        comm = communication_controller.Communication_Controller()
        #data.create_file('test.txt')

        data.lock_file('./data/test.txt')
        data.save_file('./data/test.txt', 'Another test content')
        print data.show_changes('./data/test.txt')
        print data.read_file('./data/test.txt')
        print 'sourceBox server is running'
        self.command_loop()

    def command_loop(server):

        while True:
            pass


sourceBoxServer = SourceBoxServer()
