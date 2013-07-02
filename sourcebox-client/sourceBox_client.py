#import FileSystemControllerTest
import CommunicationControllerClient
import filesystem_controller
import sys

class ClientBox(object):
    """description of class"""


    # Creates a new instance of the ClientTest
    def __init__(self):
        try:
            self.comm = CommunicationControllerClient.CommunicationControllerClient(self)
            self.fs = filesystem_controller.Filesystem_Controller(config.boxPath)
            print 'Client is running'    

        # unexpected exit
        except KeyboardInterrupt:
            print 'Terminating Client'
            del self.data
            del self.comm
            del self.fs
            del self

