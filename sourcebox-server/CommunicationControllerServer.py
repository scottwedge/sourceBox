#
# Communication_Controller
# handles the communication with the clients
#
# @encode  UTF-8, tabwidth = , newline = LF
# @author  Paul
#


import socket
import os.path
import thread
import sys

class CommunicationControllerServer(object):
    """description of class"""

    # Client initiates the action and send a command to the server
    COMMAND_SENDCREATEFILE = 'SendCreateFile'
    COMMAND_SENDLOCKFILE = 'SendLockFile'
    COMMAND_SENDUNLOCKFILE = 'SendUnLockFile'
    COMMAND_SENDMODIFYFILE = 'SendModifyFile'
    COMMAND_SENDDELETEFILE = 'SendDeleteFile'
    COMMAND_SENDMOVEFILE = 'SendMoveFile'    
    # Server initiates the action and send a command to the client
    COMMAND_GETCREATEFILE = 'GetCreateFile'
    COMMAND_GETLOCKFILE = 'GetLockFile'    
    COMMAND_GETUNLOCKFILE = 'GetUnlockFile'
    COMMAND_GETMODIFYFILE = 'GetModifyFile'
    COMMAND_GETDELETEFILE = 'GetDeleteFile'
    COMMAND_GETMOVEFILE = 'GetMoveFile'    
    COMMAND_GETVERSION = 'GetVersion'
    COMMAND_GETFILESIZE = 'GetFileSize'
    COMMAND_GETFILE = 'GetFile'
    COMMAND_GETCLOSE = 'GetClose'

    VERSION = "ver1.0"
    computer_name = 'ServerName ' + VERSION

    def __init__(self, parent):
        print 'Server Created Communication_Controller'

        # The sourceBox server is now accessible through the instance variable
        # "parent"
        self.parent = parent

        # Wait for incoming events
        thread.start_new_thread(self._command_loop, (
            'Communication_Controller Thread for ' + self.computer_name,))
    
    ## Deconstructor  
    def __del__(self):
        print 'Deconstruction Communication_Controller'
        self.s.sendall('BYE')
        self.s.close()
        self.parent.remove_client(self)
        thread.exit()

    # Waits for commands
    def _command_loop(self, thread_name):
        try:
            print '[' + thread_name + '] ' + 'Created thread: ' + thread_name

            self._create_socket()

            while True:
                data = self.s.recv(1024)
                cmd = data[:data.find(' ')]
                self._parse_command(cmd, data)
        except:
            print "_command_loop Unexpected error:", sys.exc_info()[0]    
            raise

    # Creates the socket
    def _create_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('', 50000))
        self.sock.listen(1)
        self.s, self.a = self.sock.accept()

    # Parse the command
    def _parse_command(self, cmd, data):
        if cmd == self.COMMAND_SENDCREATEFILE:
            self._send_create_file(data)
        elif cmd == self.COMMAND_SENDLOCKFILE:
            self._send_lock_file(data)
        elif cmd == self.COMMAND_SENDUNLOCKFILE:
            self._send_unlock_file(data)
        elif cmd == self.COMMAND_SENDDELETEFILE:
            self._send_delete_file(data)
        elif cmd == self.COMMAND_SENDMODIFYFILE:
            self._send_modify_file(data)
        elif cmd == self.COMMAND_SENDMOVEFILE:
            self._send_move_file(data)

        elif cmd == self.COMMAND_GETLOCKFILE:
            self._get_lock_file(data)
        elif cmd == self.COMMAND_GETMODIFYFILE:
            self._get_modify_file(data)
        elif cmd == self.COMMAND_GETUNLOCKFILE:
            self._get_unlock_file(data)
        elif cmd == self.COMMAND_GETDELETEFILE:
            self._get_delete_file(data)
        elif cmd == self.COMMAND_GETMOVEFILE:
            self._get_move_file(data)
        elif cmd == self.COMMAND_GETFILE:
            # self._get_file(data)
            pass
        elif cmd == self.COMMAND_GETVERSION:
            self._get_version()
        elif cmd == self.COMMAND_GETFILESIZE:
            self._get_file_size(data)
        elif cmd == self.COMMAND_GETCLOSE:
            self._get_close()
        else:
            print '[WARNING] recieved unknown command: ' + cmd

    # Client initiates the action and send a command to the server
    def _send_create_file(self, data):
        arrStr = data.split(' ', 2)
        cmd = arrStr[0]
        size = int(arrStr[1])
        filePath = arrStr[2]
        if len(filePath) == 0 or size < 0:
            self.s.sendall('KO')
            return 
        else:
            self.s.sendall('ok')
            content = ''
            while size > len(content):
                data = self.s.recv(1024)
                if not data:
                    break
                content += data
            self.s.sendall('ok')
            # 
            answer = self.parent.create_file(filePath, content)
            if answer == True:
                self.s.sendall('filecreated')
            else:
                self.s.sendall('createdfail')
            return

    def _send_lock_file(self, data):
        arrStr = data.split(' ', 1)
        cmd = arrStr[0]
        filePath = arrStr[1]
        if len(filePath) == 0:
            self.s.sendall('KO')
            return 
        else:
            self.s.sendall('ok')            
            # 
            answer = self.parent.lock_file(filePath)
            if answer == True:
                self.s.sendall('filelocked')
            else:
                self.s.sendall('lockedfail')
            return

    def _send_unlock_file(self, data):
        arrStr = data.split(' ', 1)
        cmd = arrStr[0]
        filePath = arrStr[1]
        if len(filePath) == 0:
            self.s.sendall('KO')
            return 
        else:
            self.s.sendall('ok')            
            # 
            answer = self.parent.unlock_file(filePath)
            if answer == True:
                self.s.sendall('fileunlocked')
            else:
                self.s.sendall('unlockedfail')
            return

    def _send_delete_file(self, data):
        arrStr = data.split(' ', 1)
        cmd = arrStr[0]
        filePath = arrStr[1]
        if len(filePath) == 0:
            self.s.sendall('KO')
            return 
        else:
            self.s.sendall('ok')            
            # 
            answer = self.parent.delete_file(filePath)
            if answer == True:
                self.s.sendall('filedeleted')
            else:
                self.s.sendall('deletedfail')
            return


    def _send_modify_file(self, data):
        arrStr = data.split(' ', 2)
        cmd = arrStr[0]
        size = int(arrStr[1])
        filePath = arrStr[2]
        if len(filePath) == 0 or size < 0:
            self.s.sendall('KO')
            return 
        else:
            self.s.sendall('ok')
            content = ''
            while size > len(content):
                data = self.s.recv(1024)
                if not data:
                    break
                content += data
            self.s.sendall('ok')
            # 
            answer = self.parent.modify_file(filePath, content)
            if answer == True:
                self.s.sendall('filemodified')
            else:
                self.s.sendall('modifiedfail')
            return
    #
    def _send_move_file(self, data):
        arrStr = data.split(' ', 1)
        cmd = arrStr[0]
        oldfilePath = arrStr[1]
        if len(oldfilePath) == 0:
            self.s.sendall('KO')
            return 
        else:
            self.s.sendall('ok')            
            # 
            newfilePath = self.s.recv(1024)
            if len(oldfilePath) == 0:
                self.s.sendall('KO')
                return
            else:
                self.s.sendall('ok')
                answer = self.parent.move_file(oldfilePath, newfilePath)
                if answer == True:
                    self.s.sendall('filemoved')
                else:
                    self.s.sendall('movedfail')
                return
        return 


    def _get_lock_file(self, data):
        cmd, path, name = data.split()
        self.s.sendall('ok')
        answer = self.parent.lock_file(path, name)
        if answer == True:
            self.s.sendall('filelocked_')
        else:
            self.s.sendall('lockedfail')



    def _get_unlock_file(self, data):
        cmd, path, name = data.split()
        self.s.sendall('ok')
        answer = self.parent.unlock_file(path, name)
        if answer == True:
            self.s.sendall('fileunlocked')
        else:
            self.s.sendall('unlockedfail')

    def _get_delete_file(self, data):
        cmd, path, name = data.split()
        self.s.sendall('ok')
        answer = self.parent.delete_file(path, name)
        if answer == True:
            self.s.sendall('filedeleted')
        else:
            self.s.sendall('deletedfail')
    
    def _get_move_file(self, data):
        cmd, oldpath, name, newpath = data.split()
        self.s.sendall('ok')
        answer = self.parent.move_file(oldpath, name, newpath)
        if answer == True:
            self.s.sendall('filemoved')
        else:
            self.s.sendall('movefail')

    def _get_file_size(self, data):
        cmd, fileName = data.split()
        filePathBase = os.path.dirname(__file__)
        size = self.parent.get_file_size(filePathBase, fileName)
        self.s.sendall(str(size))

    def _get_file(self, data):
        cmd, fileName = data.split()
        filePathBase = os.path.dirname(__file__)
        filePath = os.path.join(filePathBase, fileName)
        print "filepath", filePath
        self.s.sendall('ok')
        with open(filePath, 'rb') as f:
            data = f.read()
            self.s.sendall('%16d' % len(data))
            self.s.sendall(data)
            self.s.recv(2)

    def _get_version(self):
        self.s.sendall(self.VERSION)

    def _get_close(self):
        print 'Closing connection'
        self.s.sendall('BYE')
        self.s.close()
        self.parent.remove_client(self)
        thread.exit()

    # Server initiates the action and send a command to client
    def send_update_file(self, path, name, size, content):
        self.s.sendall(self.COMMAND_SENDMODIFYFILE + ' ' +
                       path + ' ' + name + ' ' + size)
        self.s.recv(2)
        self.s.sendall(content)
        answer = self.s.recv(11)
        if answer == 'fileupdated':
            return True
        else:
            return False

    #def send_create_file(self, path, name, size, content):
    #    self.s.sendall(
    #        self.COMMAND_SENDCREATEFILE + ' ' + path + ' ' + name + ' ' + size)
    #    ok = self.s.recv(2)
    #    if ok == 'ok':
    #        self.s.sendall(content)
    #        contenttransferd = self.s.recv(2)
    #        if contenttransferd == 'ok':  
    #            answer = self.s.recv(11)
    #            if answer == 'filecreated':
    #                return True
    #            else:
    #                return False
    #        return 'Communication Problem'

    



    def send_delete_file(self, path, name):
        self.s.sendall(self.COMMAND_SENDDELETEFILE + ' ' + path + ' ' + name)
        self.s.recv(2)
        answer = self.s.recv(11)
        if answer == 'filedeleted':
            return True
        else:
            return False

    def send_move_file(self, oldpath, name, newpath):
        self.s.sendall(self.COMMAND_SENDMOVEFILE + ' ' + oldpath + ' ' + name + ' ' + newpath )
        self.s.recv(2)
        answer = self.s.recv(11)
        if answer == 'filemoved':
            return True
        else:
            return False

