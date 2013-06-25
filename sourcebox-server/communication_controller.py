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
		parent.data.lock_file('./data/test.txt')
		self.parent = parent
		
    def update_files(self):
        self.parent.update_file('./data/test.txt')
        

    # pull functions (response)
    def create_file(self):
        self.parent.create_fiel('./data/test.txt')
        

    def lock_file(self):
        self.parent.lock_file('./data/test.txt')
        

    def modify_file(self):
        parent.modify_file('./data/test.txt')
        

    def unlock_file(self):
        parent.unlock_file('./data/test.txt')
        

    def delete_file(self):
        parent.delete_file('./data/test.txt')
        

    # Internal functions
    def _create_socket(self):
        pass
