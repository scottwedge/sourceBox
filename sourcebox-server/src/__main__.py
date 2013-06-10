#
# sourcebox-server
#
#
#

import communication_controller
import data_controller


class SourceBoxServer(object):

    def __init__(self):
        data = data_controller.Data_Controller()
        comm = communication_controller.Communication_Controller()
        print 'sourceBox server is running'
        self.command_loop()

    def command_loop(server):
        while True:
            pass


sourceBoxServer = SourceBoxServer()
