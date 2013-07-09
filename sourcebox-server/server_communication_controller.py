#
# Communication_Controller
# handles the communication with the clients
#
# @encode  UTF-8, tabwidth = , newline = LF
# @author  Paul
import thread
import threading
import socket
import logging
from urllib import pathname2url, url2pathname 


class Server_Communication_Controller(object):

    # command constants
    COMMAND_GETCREATEFILE = 'CREATE_FILE'
    COMMAND_SENDLOCKFILE = 'LOCK'
    COMMAND_SENDUNLOCKFILE = 'UNLOCK'
    COMMAND_SENDMODIFYFILE = 'MODIFY'
    COMMAND_SENDDELETEFILE = 'REMOVE'
    COMMAND_MOVE = 'MOVE'
    COMMAND_SENDCREATEDIR = 'CREATE_DIR'
    COMMAND_DELETEDIR = 'DELETE_DIR'
    COMMAND_CONNECTIONCLOSE = 'CLOSE'

    COMMAND_OK = "OK\n"
    VERSION = "1.0"

    # Constructor
    # @param parent the parent object. The sourceBox server object
    # @param connection the connection to the client
    # @param computer_name the computer_name of the client
    def __init__(self, parent, connection, computer_name):
        # catch logging object
        self.log = logging.getLogger("server")

        self.log.info(
            'Server Created Communication_Controller for ' + computer_name)

        # The sourceBox server is now accessible through the instance variable
        # "parent"
        self.parent = parent
        self.connection = connection
        self.computer_name = computer_name

        # Create OK Event (which is fired when a ok is recieved)
        self.ok = threading.Event()

        # Wait for incoming events
        thread.start_new_thread(self._command_loop, (
            'Thread ' + self.computer_name, self.connection))

    # Deconstructor
    def __del__(self):
        self.log.debug('Deconstruction Communication_Controller')
        self.connection.close()

    # Waits for (incoming) commands
    def _command_loop(self, thread_name, connection):
        try:
            self.log.info(
                '[' + thread_name + '] ' + 'Created thread: ' + thread_name)

            while True:
                data = connection.recv(1024).split(' ')
                cmd = data[0]
                self._parse_command(cmd, data)
        except socket.error, e:
            if e.errno == 104:
                self.log.warning('Client closed connection unexpectedly ')
                self.parent.remove_client(self)
                connection.close()
                thread.exit()
            else:
                self.log.error("_command_loop error: " + e.string)

    # Parse the command
    def _parse_command(self, cmd, data):
        self.log.debug('Recieved Command from the client '  + self.computer_name + ': ' + data[0])
        if cmd == self.COMMAND_GETCREATEFILE:
            self._get_create_file(data)
        elif cmd == self.COMMAND_SENDLOCKFILE:
            self._get_lock_file(data)
        elif cmd == self.COMMAND_SENDUNLOCKFILE:
            self._get_unlock_file(data)
        elif cmd == self.COMMAND_SENDDELETEFILE:
            self._get_delete_file(data)
        elif cmd == self.COMMAND_SENDMODIFYFILE:
            self._get_modify_file(data)
        elif cmd == self.COMMAND_MOVE:
            self._get_move(data)
        elif cmd == self.COMMAND_SENDCREATEDIR:
            self._get_create_dir(data)
        elif cmd == self.COMMAND_DELETEDIR:
            self._get_delete_dir(data)        
        elif cmd == self.COMMAND_CONNECTIONCLOSE:
            self._close_connection()
        elif cmd == 'OK\n':
            self.ok.set()
        else:
            self.log.warning('recieved unknown command: ' + cmd)

    # closes the connection to the client
    def _close_connection(self):
        self.connection.send('OK\n')
        self.connection.close()
        self.parent.remove_client(self.computer_name)
        thread.exit()

    # server notifies the client about a new file (uploaded by another user)
    # @param size the size of the file
    # @param path the path to the file (relative to the source box)
    def send_create_file(self, size, path, content):
        try:
            self.log.debug('Sending CREATE to client ' + self.computer_name)
            mess = "CREATE" + ' ' + str(size) + ' ' + pathname2url(path)

            self.connection.send(mess)

            # Wait for the recieve thread to send us a ok Event
            status = self.ok.wait(8.0)
            self.ok.clear()
            if not status:
                raise IOError(
                    'Did not recieve a response from the client ' + self.computer_name)
            if not size == 0:
                self.connection.send(content)
                self.log.debug("send content to client")
                # Wait for the recieve thread to send us a ok Event
                status = self.ok.wait(8.0)
                self.ok.clear()
                if not status:
                    raise IOError(
                        'Did not recieve a response from the client ' + self.computer_name)

           # self.log.debug('Hello. Creation worked. The client said he is ok :)')
        except IOError, err:
            self.log.error(str(err))
        # NOTE
        # Any notification would be eaten by the server command loop at the moment.
        # We need a event solution similar to the client if we are interested in the
        # successful execution of the file. Like the code above.

    #
    def send_close(self):
        self.connection.send('CLOSE\n')
        status = self.ok.wait(8.0)
        self.ok.clear()
        if not status:
            raise IOError(
                'Did not recieve a response from the the client ' + self.computer_name)
        self.connection.close()

    # server notifies the client about delete file (initiated by another user)
    # @param path the path to the file (relative to the source box)
    def send_delete_file(self, path):
        self.log.debug('Sending REMOVE to client ' + self.computer_name)
        mess = "REMOVE" + ' ' + pathname2url(path)

        self.connection.send(mess)

        # Wait for the recieve thread to send us a ok Event
        status = self.ok.wait(8.0)
        self.ok.clear()
        if not status:
            raise IOError(
                'Did not recieve a response from the the client ' + self.computer_name)

       # self.log.debug('Hello. Delete worked. The client said he is ok :)')

    # server notifies the client about modify file (initiated by another user)
    # @param path the path to the file (relative to the source box)
    def send_modify_file(self, size, path, content):
        self.log.debug('Sending MODIFY to client ' + self.computer_name)
        mess = "MODIFY" + ' ' + str(size) + ' ' + pathname2url(path)

        self.connection.send(mess)

        # Wait for the recieve thread to send us a ok Event
        status = self.ok.wait(8.0)
        self.ok.clear()
        if not status:
            raise IOError(
                'Did not recieve a response from the client ' + self.computer_name)
        if not size == 0:
            self.connection.send(content)

            # Wait for the recieve thread to send us a ok Event
            status = self.ok.wait(8.0)
            self.ok.clear()
            if not status:
                raise IOError(
                    'Did not recieve a response from the client ' + self.computer_name)

       # self.log.debug('Hello. Modifying worked. The client said he is ok :)')

    # server notifies the client about lock file (initiated by another user)
    # @param path the path to the file (relative to the source box)
    def send_lock_file(self, path):
        try:
            self.log.debug('Sending LOCK to client' + self.computer_name)
            mess = "LOCK" + ' ' + pathname2url(path)

            self.connection.send(mess)

            # Wait for the recieve thread to send us a ok Event
            status = self.ok.wait(8.0)
            self.ok.clear()
            if not status:
                raise IOError(
                    'Did not recieve a response from the client.' + self.computer_name)

           # self.log.debug('Hello. Locking worked. The client said he is ok :)')
        except IOError, err:
            self.log.error(str(err))

    # server notifies the client about unlock file (initiated by another user)
    # @param path the path to the file (relative to the source box)
    def send_unlock_file(self, path):
        self.log.debug('Sending UNLOCK to client' + self.computer_name)
        mess = "UNLOCK" + ' ' + pathname2url(path)
        try:
            self.connection.send(mess)

            # Wait for the recieve thread to send us a ok Event
            status = self.ok.wait(8.0)
            self.ok.clear()
            if not status:
                raise IOError(
                    'Did not recieve a response from the client ' + self.computer_name)

           ## self.log.debug(
            #    'Hello. Unlocking worked. The client said he is ok :)')
        except IOError, err:
            self.log.error(str(err))

    # server notifies the client about a new Dir (initiated by another user)
    # @param path the path to the file (relative to the source box)
    def send_create_dir(self, path):
        try:
            self.log.debug('Sending CREATE_DIR to client' + self.computer_name)
            mess = "CREATE_DIR" + ' ' + pathname2url(path)

            self.connection.send(mess)

            # Wait for the recieve thread to send us a ok Event
            status = self.ok.wait(8.0)
            self.ok.clear()
            if not status:
                raise IOError(
                    'Did not recieve a response from the client.' + self.computer_name)
        except IOError, err:
            self.log.error(str(err))


    # server notifies the client about a deleted Dir (initiated by another user)
    # @param path the path to the file (relative to the source box)
    def send_delete_dir(self, path):
        try:
            self.log.debug('Sending DELETE_DIR to client' + self.computer_name)
            mess = "DELETE_DIR" + ' ' + pathname2url(path)

            self.connection.send(mess)

            # Wait for the recieve thread to send us a ok Event
            status = self.ok.wait(8.0)
            self.ok.clear()
            if not status:
                raise IOError(
                    'Did not recieve a response from the client.' + self.computer_name)
        except IOError, err:
            self.log.error(str(err))

    # server notifies the client about a moved Dir (initiated by another user)
    def send_move(self, old_file_path, new_file_path):
        try:
            self.log.debug('Sending MOVE to client' + self.computer_name)
            mess = "MOVE" + ' ' + pathname2url(old_file_path) + ' ' + pathname2url(new_file_path)

            self.connection.send(mess)

            # Wait for the recieve thread to send us a ok Event
            status = self.ok.wait(8.0)
            self.ok.clear()
            if not status:
                raise IOError(
                    'Did not recieve a response from the client.' + self.computer_name)
        except IOError, err:
            self.log.error(str(err))

    # client sends a CREATE_FILE command to the server
    # @param data a data array

    def _get_create_file(self, data):
        communication_data = self._recieve_command_with_content(data)

        # send create_file function to the server
        answer = self.parent.create_file(communication_data['file_path'], communication_data['file_size'], self.computer_name, communication_data['content'])
        if answer:
            self.connection.send('OK\n')

    # client sends a LOCK command to the server
    # @param data a data array
    def _get_lock_file(self, data):
        communication_data = self._recieve_command(data)

        answer = self.parent.lock_file(communication_data['file_path'], self.computer_name)
        if answer:
            self.connection.send('OK\n')

    # client sends a UNLOCK command to the server
    # @param data a data array
    def _get_unlock_file(self, data):
        communication_data = self._recieve_command(data)
        answer = self.parent.unlock_file(communication_data['file_path'], self.computer_name)
        if answer == True:
            self.connection.send('OK\n')
        else:
            self.connection.send('ERROR\n')
    # client sends a REMOVE command to the server
    # @param data a data array

    def _get_delete_file(self, data):
        communication_data = self._recieve_command(data)
        answer = self.parent.delete_file(communication_data['file_path'], self.computer_name)
        if answer:
            self.connection.send('OK\n')
        else:
            self.connection.send('ERROR\n')

    # the client sends a MODIFY command
    # @param data a data array
    def _get_modify_file(self, data):
        communication_data = self._recieve_command_with_content(data)

        answer = self.parent.modify_file(communication_data['file_path'], communication_data['content'], self.computer_name)
        if answer:
            self.connection.send('OK\n')

    # the client sends a MOVE command
    # @param data a data array
    def _get_move(self, data):
        old_file_path = url2pathname(data[1])
        new_file_path = url2pathname(data[2])

        # check if the data string is correct
        if len(old_file_path) == 0 or len(new_file_path) == 0:
            self.connection.send('ERROR\n')
        else:
            answer = self.parent.move(old_file_path, new_file_path, self.computer_name)
            if answer:
                self.connection.send('OK\n')

    # the client sends a CREATE_DIR command
    # @param data a data array
    def _get_create_dir(self, data):
        communication_data = self._recieve_command(data)
        answer = self.parent.create_dir(communication_data['file_path'], self.computer_name)
        if answer:
            self.connection.send('OK\n')
        else:
            self.connection.send('ERROR\n')

    # the client sends a DELETE_DIR command
    # @param data a data array
    def _get_delete_dir(self, data):
        communication_data = self._recieve_command(data)
        answer = self.parent.delete_dir(communication_data['file_path'], self.computer_name)
        if answer:
            self.connection.send('OK\n')
        else:
            self.connection.send('ERROR\n')

    # helper function
    # @param data a data array
    # @returns a dictionary like { 'command' : command, 'file_path' :  file_path} or None (if error)
    def _recieve_command(self, data):
        command = data[0]
        self.log.debug('Recieved ' + str(data))
        file_path = url2pathname(data[1])
        self.log.debug('Recieve command ' + str(file_path))

        if len(file_path) == 0:
            self.connection.send('ERROR\n')
            return None
        else:
            return {'command': command, 'file_path':  file_path}

    # helper function
    # @param data a data array
    # @returns a dictionary like { 'command' : command, 'file_size' : file_size, 'file_path' :  file_path, 'content' : content}
    def _recieve_command_with_content(self, data):
        self.log.debug('Recieved ' + str(data))
        command = data[0]
        file_size = int(data[1])
        file_path = url2pathname(data[2])

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

        return {'command': command, 'file_size': file_size, 'file_path':  file_path, 'content': content}
