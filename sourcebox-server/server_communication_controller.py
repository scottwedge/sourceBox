#
# Communication_Controller
# handles the communication with the clients
#
# @encode  UTF-8, tabwidth = , newline = LF
# @author  Paul
import thread
import socket

class Server_Communication_Controller(object):

    # command constants
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

    ## Constructor
    # @param parent the parent object. The sourceBox server object
    # @param connection the connection to the client
    # @param computer_name the computer_name of the client
    def __init__(self, parent, connection, computer_name):
        print 'Server Created Communication_Controller'

        # The sourceBox server is now accessible through the instance variable
        # "parent"
        self.parent = parent
        self.connection = connection
        self.computer_name = computer_name

        # Wait for incoming events
        thread.start_new_thread(self._command_loop, (
            'Communication_Controller Thread for ' + self.computer_name, self.connection))
    
    ## Deconstructor  
    def __del__(self):
        print 'Deconstruction Communication_Controller'
        self.connection.sendall('BYE')
        self.connection.close()
        self.parent.remove_client(self)
        thread.exit()

    ## Waits for (incoming) commands
    def _command_loop(self, thread_name, connection):
        try:
            print '[' + thread_name + '] ' + 'Created thread: ' + thread_name

            while True:
                data = connection.recv(1024).split(' ')
                cmd = data[0]
                self._parse_command(cmd, data)
        except socket.error, e:
            if e.error == 104:
                print '[WARNING] client closed connection unexpectedly'
                self.parent.remove_client(self)
                connection.close()
                thread.exit()
            else:
                print "_command_loop error:" + e.string  


    # Parse the command
    def _parse_command(self, cmd, data):
        print '[DEBUG] Recieved Command from the client: ' + data[0]
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

    ## closes the connection to the client
    def _close_connection(self):
        self.parent.remove_client(self)
        self.connection.sendall('BYE')
        self.connection.close()
        thread.exit()

    ## server notifies the client about a new file (uploaded by another user)
    # @param size the size of the file
    # @param path the path to the file (relative to the source box)
    def send_create_file(self, size, path):
        print 'Sending CREATE to client'
        mess = "CREATE" + ' ' + str(size) + ' ' + path

        self.connection.send(mess)

        # Any notification would be eaten by the server command loop at the moment.
        # We need a event solution similar to the client if we are interested in the
        # successful execution of the file

    ## client sends a CREATE_FILE command to the server
    # @param data a data array
    def _get_create_file(self, data):
        communication_data = self._recieve_command_with_content(data)
 
        # send create_file function to the server
        answer = self.parent.create_file('', communication_data['file_path'], communication_data['content'], self.computer_name)
        if answer:
            self.connection.send('OK\n')

    ## client sends a LOCK command to the server
    # @param data a data array
    def _get_lock_file(self, data):
        communication_data = self._recieve_command(data)
      
        answer = self.parent.lock_file('', communication_data['file_path'])
        if answer: self.connection.send('OK\n')            

    ## client sends a UNLOCK command to the server
    # @param data a data array
    def _get_unlock_file(self, data):
        communication_data = self._recieve_command(data)
        answer = self.parent.unlock_file('.', communication_data['file_path'])
        if answer == True:
            self.connection.send('OK\n')            
        else:
            self.connection.send('ERROR\n')
    ## client sends a REMOVE command to the server
    # @param data a data array
    def _get_delete_file(self, data):
        communication_data = self._recieve_command(data)
        answer = self.parent.delete_file('.', communication_data['file_path'])
        if answer:
            self.connection.send('OK\n')            
        else:
            self.connection.send('ERROR\n')

    ## the client sends a MODIFY command
    # @param data a data array
    def _get_modify_file(self, data):
        communication_data = self._recieve_command_with_content(data)

        answer = self.parent.modify_file('.', communication_data['file_path'], communication_data['content'])
        if answer: self.connection.send('OK\n')

    ## the client sends a MOVE command
    # @param data a data array
    def _get_move_file(self, data):
        old_file_path = data[1]
        new_file_path = data[2]

        # check if the data string is correct
        if len(old_file_path) == 0 or len(new_file_path) == 0:
            self.connection.send('ERROR\n')
        else:
            answer = self.parent.move_file(old_file_path, new_file_path)
            if answer: self.connection.send('OK\n')



    ## the client sends a CREATE_DIR command
    # @param data a data array
    def _get_create_dir(self, data):
        communication_data = self._recieve_command(data)
        answer = self.parent.create_dir(communication_data['file_path'])
        if answer:
            self.connection.send('OK\n')            
        else:
            self.connection.send('ERROR\n')

    ## helper function
    # @param data a data array
    # @returns a dictionary like { 'command' : command, 'file_path' :  file_path}
    def _recieve_command(self, data):
        command = data[0]
        file_path = data[1]

        if len(file_path) == 0:
            self.connection.send('ERROR\n')
        else:
            answer = self.parent.delete_file('.', file_path)
            if answer:
                self.connection.send('OK\n')            
            else:
                self.connection.send('ERROR\n')

        return { 'command' : command, 'file_path' :  file_path}

    ## helper function
    # @param data a data array
    # @returns a dictionary like { 'command' : command, 'file_size' : file_size, 'file_path' :  file_path, 'content' : content}
    def _recieve_command_with_content(self, data):

        command = data[0]
        file_size = int(data[1])
        file_path = data[2]

        # check if the data string is correct
        if len(file_path) == 0 or file_size < 0:
            self.connection.send('ERROR\n')
            return 
        else:
            # return OK to the client. Client can initiate data transfer now.
            self.connection.send('OK\n')

            # read data from the socket
            content = ''
            while file_size > len(content):
                data = self.connection.recv(1024)
                if not data:
                    break
                content += data

        return { 'command' : command, 'file_size' : file_size, 'file_path' :  file_path, 'content' : content}
