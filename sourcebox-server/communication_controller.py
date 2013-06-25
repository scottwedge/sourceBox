#
# Communication_Controller
# handles the communication with the clients
#
# @encode  UTF-8, tabwidth = , newline = LF
# @author  Paul
#


# push functions (requests)


class Communication_Controller(object):

    def __init__(self, parent):
		print 'Created Communication_Controller'
		#parent.data.lock_file(file_name)
		self.parent = parent
		
    def update_files(self, file_name):
        self.parent.update_file(file_name)
        

    # pull functions (response)
    def create_file(self, file_name):
        self.parent.create_file(file_name)
        

    def lock_file(self, file_name):
        self.parent.lock_file(file_name)
        

    def modify_file(self, file_name):
        self.parent.modify_file(file_name)
        

    def unlock_file(self, file_name):
        self.parent.unlock_file(file_name)
        

    def delete_file(self, file_name):
        self.parent.delete_file(file_name)
        

    # Internal functions
    def _create_socket(self):
        pass
