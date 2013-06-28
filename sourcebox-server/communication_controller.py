#
# Communication_Controller
# handles the communication with the clients
#
# @encode  UTF-8, tabwidth = , newline = LF
# @author  Paul
#

class Communication_Controller(object):
    computer_name = None
    import socket
    import os.path


    COMMAND_SENDUPDATEFILE = 'SendUpdateFile'
    COMMAND_SENDCREATEFILE = 'SendCreateFile'
    COMMAND_SENDDELETEFILE = 'SendDeleteFile'
    COMMAND_GETCREATEFILE = 'GetCreateFile'
    COMMAND_GETLOCKFILE = 'GetLockFile'
    COMMAND_GETMODIFYFILE = 'GetModifyFile'
    COMMAND_GETUNLOCKFILE = 'GetUnlockFile'
    COMMAND_GETDELETEFILE = 'GetDeleteFile'
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

        while True:
            data = s.recv(1024)
            cmd = data[:data.find(' ')]

            if cmd == COMMAND_GETCREATEFILE:
                cmd, path, name, size = data.split()
                s.sendall('ok')
                content = ''
                while size > len(content):
                    data = sock.recv(1024)
                    if not data: 
                        break
                    content += data
                s.sendall('ok')
                answer = _get_create_file(self, path, name, content)
                if answer == true:
                    s.sendall('filecreated')
                else:
                    s.sendall('createdfail')

            if cmd == COMMAND_GETLOCKFILE:
                cmd, path, name = data.split()
                s.sendall('ok')
                answer = _get_lock_file(self, path, name)
                if answer == true:
                    s.sendall('filelocked_')
                else:
                    s.sendall('lockedfail')
            
            if cmd == COMMAND_GETMODIFYFILE:
                cmd, path, name, size = data.split()
                s.sendall('ok')
                content = ''
                while size > len(content):
                    data = sock.recv(1024)
                    if not data: 
                        break
                    content += data
                s.sendall('ok')
                answer = _get_modify_file(self, path, name, content)
                if answer == true:
                    s.sendall('filemodified')
                else:
                    s.sendall('modifiedfail')

            if cmd == COMMAND_GETUNLOCKFILE:
                cmd, path, name = data.split()
                s.sendall('ok')
                answer = _get_unlock_file(self, path, name)
                if answer == true:
                    s.sendall('fileunlocked')
                else:
                    s.sendall('unlockedfail')

            if cmd == COMMAND_GETDELETEFILE:
                cmd, path, name = data.split()
                s.sendall('ok')
                answer = _get_delete_file(self, path, name)
                if answer == true:
                    s.sendall('filedeleted')
                else:
                    s.sendall('deletedfail')



            #if cmd == COMMAND_GETFILE:
            #            cmd, fileName = data.split()
            #            filePathBase = os.path.dirname(__file__)
            #            filePath = os.path.join(filePathBase, fileName)
            #            print "filepath", filePath
            #            s.sendall('ok')
            #            with open(filePath, 'rb') as f:
            #                data = f.read()
            #            s.sendall('%16d' % len(data))
            #            s.sendall(data)
            #            s.recv(2)

            if cmd == COMMAND_GETVERSION: 
                s.sendall(VERSION)
    
            if cmd == COMMAND_GETFILESIZE: 
                cmd, fileName = data.split()
                filePathBase = os.path.dirname(__file__)
                filePath = os.path.join(filePathBase, fileName)
                size = GetFileSizeDirect(filePath)
                s.sendall(str(size))
                
        

    # Server initiates the action and send a command to client
    def send_update_file(self, path, name, size, content):
        s.sendall(COMMAND_SENDUPDATEFILE + ' ' + path + ' ' + name + ' ' + size)
        r = s.recv(2)
        s.sendall(content)
        answer = s.recv(11)
        if answer == 'fileupdated':
            return true
        else:
            return false

    def send_create_file(self, path, name, size, content):
        s.sendall(COMMAND_SENDCREATEFILE + ' ' + path + ' ' + name + ' ' + size)
        r = s.recv(2)
        s.sendall(content)
        answer = s.recv(11)
        if answer == 'filecreated':
            return true
        else:
            return false

    def send_delete_file(self, path, name):
        s.sendall(COMMAND_SENDDELETEFILE + ' ' + path + ' ' + name)
        r = s.recv(2)
        answer = s.recv(11)
        if answer == 'filedeleted':
            return true
        else:
            return false

    # Client initiated the action and sent a command to Server

    def _get_create_file(self, path, name, content):
        answer = self.parent.create_file(path, name, content)
        return answer

    def _get_lock_file(self, path, name):
        answer = self.parent.lock_file(path, name)
        return answer
        

    def _get_modify_file(self, path, name, content):
        answer = self.parent.modify_file(path, name, content)
        return answer

    def _get_unlock_file(self, path, name):
        answer = self.parent.unlock_file(path, name)
        return answer
        

    def _get_delete_file(self, path, name):
        answer = self.parent.delete_file(path, name)
        return answer

    # Internal functions
   
    def _PressEnterKey():
        print "Please, Press Enter Key ..."
        data = sys.stdin.readline()
        return 0

    def _GetFileSizeDirect(filePath):
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