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
        data.create_file('test.txt')

        print 'sourceBox server is running'
        self.command_loop()

    def command_loop(server):

        while True:
            pass


sourceBoxServer = SourceBoxServer()
