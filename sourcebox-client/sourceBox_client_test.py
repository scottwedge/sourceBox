#import FileSystemControllerTest
import CommunicationControllerClient
import sys

class ClientTest(object):
    """description of class"""


    # Creates a new instance of the ClientTest
    def __init__(self):
        try:
            self.comm = CommunicationControllerClient.CommunicationControllerClient(self)
            
            # Just some random tests

            # data.create_file('test.txt')
            # self.data.lock_file('./data/test.txt')
                # self.data.save_file('./data/test.txt', 'Another test content')
            # print self.data.show_changes('./data/test.txt')
            # print self.data.read_file('./data/test.txt')

            print 'ClientTest is running'    

        # unexpected exit
        except KeyboardInterrupt:
            print 'Terminating ClientTest'
            del self.data
            del self.comm
            del self

      
    def InitController(self, strIP, intPORT):
        self.comm.Init(strIP, intPORT)

    def create_file(self, filePath, content):
        size = len(content)
        resp = self.comm.send_create_file(filePath, size, content)
        return resp

    def modify_file(self, filePath, content):
        size = len(content)
        resp = self.comm.send_modify_file(filePath, size, content)
        return resp
    
    def lock_file(self, filePath):
        resp = self.comm.send_lock_file(filePath)
        return resp

    def unlock_file(self, filePath):
        resp = self.comm.send_unlock_file(filePath)
        return resp
           
    def delete_file(self, filePath):
        resp = self.comm.send_delete_file(filePath)
        return resp

    def move_file(self, oldfilePath, newfilePath):
        resp = self.comm.send_move_file(oldfilePath, newfilePath)
        return resp

    def create_dir(self, filePath):
        resp = self.comm.send_create_dir(filePath)
        return resp
    
#
def _PressEnterKey():
    print "Please, Press Enter Key ..."
    data = sys.stdin.readline()
    return 0

#start
try:
    clientTest = ClientTest()    
    clientTest.InitController('127.0.0.1', 50000)


    #
    #res = clientTest.create_file('pathTest\filenameTest.txt', 'ContentTest')
    #print 'create_file Test'
     
    #res = clientTest.lock_file('pathTest\filenameTest.txt')
    #print 'lock_file Test' 

    #res = clientTest.unlock_file('pathTest\filenameTest.txt')
    #print 'unlock_file Test' 

    #res = clientTest.delete_file('pathTest\filenameTest.txt')
    #print 'delete_file Test' 

    #res = clientTest.modify_file('pathTest\filenameTest.txt', 'ContentTest')
    #print 'modify_file Test'

    #res = clientTest.move_file('pathTest\filenameTest.txt', 'newpathTest\TEST.txt')
    #print 'move_file Test'

    res = clientTest.create_dir('pathTest\filenameTest.txt')
    print 'create_dir Test'

    #
    print 'Result', res

except:
    print "Unexpected error:", sys.exc_info()[0]    
    print 'Error_Exception Client'

finally: 
    print 'Client End'
    _PressEnterKey()