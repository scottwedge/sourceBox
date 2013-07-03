#
# Communication_Controller
# handles the communication with the clients
#
# @encode  UTF-8, tabwidth = , newline = LF
# @author  Paul
import thread
import sys

class Server_Communication_Controller(object):
    """description of class"""

    # Client initiates the action and send a command to the server
    COMMAND_GETCREATEFILE = 'CREATE_FILE'
    COMMAND_SENDLOCKFILE = 'LOCK'
    COMMAND_SENDUNLOCKFILE = 'UNLOCK'
    COMMAND_SENDMODIFYFILE = 'MODIFY'
    COMMAND_SENDDELETEFILE = 'REMOVE'
    COMMAND_SENDMOVEFILE = 'MOVE'
    COMMAND_SENDCREATEDIR = 'CREATE_DIR'
    COMMAND_CONNECTIONCLOSE = 'CLOSE'
    COMMAND_OK = "OK\n"
    VERSION = "1.0"

    def __init__(self, parent, connection, computer_name):
        print 'Server Created Communication_Controller'

        # The sourceBox server is now accessible through the instance variable
        # "parent"
        self.parent = parent
        self.connection = connection
        self.computer_name = computer_name

        # Wait for incoming events
        thread.start_new_thread(self._command_loop, (
            'COMMCTL Thread for ' + self.computer_name, self.connection))
    
    ## Deconstructor  
    def __del__(self):
        print 'Deconstruction Communication_Controller'
        self.connection.sendall('BYE')
        self.connection.close()
        self.parent.remove_client(self)
        thread.exit()

    # Waits for commands
    def _command_loop(self, thread_name, connection):
        try:
            print '[' + thread_name + '] ' + 'Created thread: ' + thread_name

            while True:
                data = connection.recv(1024)
                cmd = data[:data.find(' ')]
                self._parse_command(cmd, data)
        except:
            print "_command_loop Unexpected error:", sys.exc_info()[0]    
            raise


    # Parse the command
    def _parse_command(self, cmd, data):
        print '[DEBUG] Recieved Command from the client: ' + data
        if cmd == self.COMMAND_GETCREATEFILE:
            print 'CMD is create_file'
            self._get_create_file(data)
        elif cmd == self.COMMAND_SENDLOCKFILE:
            self._get_lock_file(data)
        elif cmd == self.COMMAND_SENDUNLOCKFILE:
            self._get_unlock_file(data)
        elif cmd == self.COMMAND_SENDDELETEFILE:
            self._get_delete_file(data)
        elif cmd == self.COMMAND_SENDMODIFYFILE:
            self._get_modify_file(data)
        elif cmd == self.COMMAND_SENDMOVEFILE:
            self._get_move_file(data)
        elif cmd == self.COMMAND_SENDCREATEDIR:
            self._get_create_dir(data)
        else:
            print '[WARNING] recieved unknown command: ' + cmd

    # 
    def _get_connection_close(self):
        self.parent.remove_client(self)
        self.connection.sendall('BYE')
        self.connection.close()
        thread.exit()

    # Server pushes data to the client
    def send_create_file(self, size, path):
        print 'Sending CREATE to client'
        mess = "CREATE" + ' ' + str(size) + ' ' + path

        self.connection.send(mess)
       # status = self.connection.recv(2) == 'OK\n'

        #if status:
        #    return 0 #True
        #else:
        #    return -3 # Sending problem


    # Client initiates the action and send a command to the server
    def _get_create_file(self, data):
        arrStr = data.split(' ', 2)
        size = int(arrStr[1])
        filePath = arrStr[2]
        if len(filePath) == 0 or size < 0:
            self.connection.send('ERROR\n')
            return 
        else:
            self.connection.send('OK\n')
            content = ''
            while size > len(content):
                data = self.connection.recv(1024)
                if not data:
                    break
                content += data

            answer = self.parent.create_file('', filePath, content, self.computer_name)
            if answer:
                self.connection.send('OK\n')


    def _get_lock_file(self, data):
        arrStr = data.split(' ', 1)
        file_name = arrStr[1]
        if len(file_name) == 0:
            self.connection.send('ERROR\n')
            return 
        else:       
            answer = self.parent.lock_file('', file_name)
            if answer: self.connection.send('OK\n')            

    def _get_unlock_file(self, data):
        arrStr = data.split(' ', 1)
        file_name = arrStr[1]
        if len(file_name) == 0:
            self.connection.send('ERROR\n')
            return 
        else:
            # 
            answer = self.parent.unlock_file('.', file_name)
            if answer == True:
                self.connection.send('OK\n')            
            else:
                self.connection.send('ERROR\n')

    def _get_delete_file(self, data):
        arrStr = data.split(' ', 1)
        file_name = arrStr[1]
        if len(file_name) == 0:
            self.connection.send('ERROR\n')
        else:
            answer = self.parent.delete_file('.', file_name)
            if answer:
                self.connection.send('OK\n')            
            else:
                self.connection.send('ERROR\n')


    def _get_modify_file(self, data):
        arrStr = data.split(' ', 2)
        size = int(arrStr[1])
        file_name = arrStr[2]
        if len(file_name) == 0 or size < 0:
            self.connection.send('ERROR')
            return 
        else:
            self.connection.send('OK\n')
            content = ''
            while size > len(content):
                data = self.connection.recv(1024)
                if not data:
                    break
                content += data
            answer = self.parent.modify_file('.', file_name, content)
            if answer: self.connection.send('OK\n')


    def _get_move_file(self, data):
        arrStr = data.split(' ', 1)
        oldfilePath = arrStr[1]
        if len(oldfilePath) == 0:
            self.connection.send('ERROR\n')
        else:
            self.connection.send('OK\n')            
            newfilePath = self.connection.recv(1024)
            if len(oldfilePath) == 0:
                self.connection.send('ERROR\n')
            else:
                answer = self.parent.move_file(oldfilePath, newfilePath)
                if answer:
                    self.connection.send('OK\n')
                else:
                    self.connection.send('ERROR\n')

    def _get_create_dir(self, data):
        arrStr = data.split(' ', 1)
        filePath = arrStr[1]
        if len(filePath) == 0:
            self.connection.send('ERROR\n')
        else:
            answer = self.parent.create_dir('.')
            if answer:
                self.connection.send('OK\n')            
            else:
                self.connection.send('ERROR\n')


