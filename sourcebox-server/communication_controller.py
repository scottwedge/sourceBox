#
# Communication_Controller
# handles the communication with the clients
#
# @encode  UTF-8, tabwidth = , newline = LF
# @author  Paul
#


# push functions (requests)


class Communication_Controller(object):
    computer_name = None
    import socket
    import os.path

    COMMAND_GETVERSION = 'GetVersion'
    COMMAND_GETFILESIZE = 'GetFileSize'
    COMMAND_GETFILE = 'GetFile'
    VERSION = "ver1.0"

    def __init__(self, parent):
        
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.bind(('', 50000))
        sock.listen(1)
        s,a = sock.accept()
        print 'Server Created Communication_Controller'
        self.parent = parent

	# Updates the file on the client
    def send_update_file(self, path):
        pass

    def send_create_file(self, path, content):
        pass

    def send_delete_file(self, path):
        pass

    # pull functions (response)
    def get_create_file(self, path):
        self.parent.create_file(path)
        

    def get_lock_file(self, path):
        self.parent.lock_file(path)
        

    def get_modify_file(self, path):
        self.parent.modify_file(path)
        

    def get_unlock_file(self, path):
        self.parent.unlock_file(path)
        

    def get_delete_file(self, path):
        self.parent.delete_file(path)
        

    # Internal functions
    def _create_socket(self):
        pass

    def PressEnterKey():
        print "Please, Press Enter Key ..."
        data = sys.stdin.readline()
        return 0

    def GetFileSizeDirect(filePath):
        if os.path.exists(filePath):
            return os.path.getsize(filePath)
        else:
            return -1

    #while True:
    #    data = s.recv(1024)
    #    cmd = data[:data.find(' ')]

    #    if cmd == COMMAND_GETVERSION: 
    #        s.sendall(VERSION)
    
    #    if cmd == COMMAND_GETFILESIZE: 
    #        cmd, fileName = data.split()
    #        filePathBase = os.path.dirname(__file__)
    #        filePath = os.path.join(filePathBase, fileName)
    #        size = GetFileSizeDirect(filePath)
    #        s.sendall(str(size))
    
    #    if cmd == COMMAND_GETFILE:
    #        cmd, fileName = data.split()
    #        filePathBase = os.path.dirname(__file__)
    #        filePath = os.path.join(filePathBase, fileName)
    #        print "filepath", filePath
    #        s.sendall('ok')
    #        with open(filePath, 'rb') as f:
    #            data = f.read()
    #        s.sendall('%16d' % len(data))
    #        s.sendall(data)
    #        s.recv(2)

    #    if cmd == 'end':
    #        s.close()
    #        break