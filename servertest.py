import unittest

class TestServer(unittest.TestCase):
	def setUp(self):
		self.server = Server()
        s = socket.socket()
        server.addr = socket.gethostname()
        port = 1234
        s.bind((self.server.addr, port))
        s.listen(5)
        self.conn, self.clientaddr = s.accept()

        self.conn = 

	def test_quit():

		self.server.quit(self.conn)



	def tearDown(self):
		pass