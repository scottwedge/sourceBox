#
# Communication_Controller
# handles the communication with the clients
#
# @encode  UTF-8, tabwidth = , newline = LF
# @author  Paul
#


# push functions (requests)


class Communication_Controller(object):
    user_ip = None

    
    def __init__(self, parent):
		print 'Created Communication_Controller'
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
