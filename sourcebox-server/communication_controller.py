#
# Communication_Controller
# handles the communication with the clients
#
# @encode  UTF-8, tabwidth = , newline = LF
# @author  Paul
#

import socket
import os.path


class Communication_Controller(object):
    computer_name = None

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
        self._create_socket()
        print 'Server Created Communication_Controller'

        # The sourceBox server is now accessible through the instance variable
        # "parent"
        self.parent = parent

        # Wait for incoming events
        self._command_loop()

    # Waits for commands
    def _command_loop(self):
        while True:
            data = self.s.recv(1024)
            cmd = data[:data.find(' ')]
            self._parse_command(cmd, data)

    # Creates the socket
    def _create_socket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('', 50000))
        sock.listen(1)
        self.s, self.a = sock.accept()

    # Parse the command
    def _parse_command(self, cmd, data):
        if cmd == self.COMMAND_GETCREATEFILE:
            cmd, path, name, size = data.split()
            self.s.sendall('ok')
            content = ''
            while size > len(content):
                data = self.sock.recv(1024)
                if not data:
                    break
                content += data
            self.s.sendall('ok')
            answer = self._get_create_file(path, name, content)
            if answer == True:
                self.s.sendall('filecreated')
            else:
                self.s.sendall('createdfail')

        elif cmd == self.COMMAND_GETLOCKFILE:
            cmd, path, name = data.split()
            self.s.sendall('ok')
            answer = self._get_lock_file(path, name)
            if answer == True:
                self.s.sendall('filelocked_')
            else:
                self.s.sendall('lockedfail')

        elif cmd == self.COMMAND_GETMODIFYFILE:
            cmd, path, name, size = data.split()
            self.s.sendall('ok')
            content = ''
            while size > len(content):
                data = self.sock.recv(1024)
                if not data:
                    break
                content += data
            self.s.sendall('ok')
            answer = self._get_modify_file(path, name, content)
            if answer == True:
                self.s.sendall('filemodified')
            else:
                self.s.sendall('modifiedfail')

        elif cmd == self.COMMAND_GETUNLOCKFILE:
            cmd, path, name = data.split()
            self.s.sendall('ok')
            answer = self._get_unlock_file(path, name)
            if answer == True:
                self.s.sendall('fileunlocked')
            else:
                self.s.sendall('unlockedfail')

        elif cmd == self.COMMAND_GETDELETEFILE:
            cmd, path, name = data.split()
            self.s.sendall('ok')
            answer = self._get_delete_file(path, name)
            if answer == True:
                self.s.sendall('filedeleted')
            else:
                self.s.sendall('deletedfail')

            # if cmd == COMMAND_GETFILE:
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
        elif cmd == self.COMMAND_GETVERSION:
            self.s.sendall(self.VERSION)

        elif cmd == self.COMMAND_GETFILESIZE:
            cmd, fileName = data.split()
            filePathBase = os.path.dirname(__file__)
            filePath = os.path.join(filePathBase, fileName)
            size = self._GetFileSizeDirect(filePath)
            self.s.sendall(str(size))
        else:
            print 'Unknown Command: ' + cmd

    # Server initiates the action and send a command to client
    def send_update_file(self, path, name, size, content):
        self.s.sendall(self.COMMAND_SENDUPDATEFILE + ' ' +
                       path + ' ' + name + ' ' + size)
        self.s.recv(2)
        self.s.sendall(content)
        answer = self.s.recv(11)
        if answer == 'fileupdated':
            return True
        else:
            return False

    def send_create_file(self, path, name, size, content):
        self.s.sendall(
            self.COMMAND_SENDCREATEFILE +
            ' ' +
            path +
            ' ' +
            name +
            ' ' +
            size)
        self.s.recv(2)
        self.s.sendall(content)
        answer = self.s.recv(11)
        if answer == 'filecreated':
            return True
        else:
            return False

    def send_delete_file(self, path, name):
        self.s.sendall(self.COMMAND_SENDDELETEFILE + ' ' + path + ' ' + name)
        self.s.recv(2)
        answer = self.s.recv(11)
        if answer == 'filedeleted':
            return True
        else:
            return False

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

    def _GetFileSizeDirect(filePath):
        if os.path.exists(filePath):
            return os.path.getsize(filePath)
        else:
            return -1
