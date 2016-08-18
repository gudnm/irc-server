import socket
import sys
import pdb

class Server:

	def __init__(self):
		self.addr = None
		self.session = None
		self.commands = {'QUIT': (0, self.quit), 'NICK': (1, self.nick), 'USER': (4, self.user)}

	def handle(self, message, conn):
		messageparts = message.split()
		print(messageparts)
		if messageparts[0] in self.commands:
			try:
				print(conn, messageparts[1:])
#				pdb.set_trace()
				self.commands[messageparts[0]][1](conn, *messageparts[1:])
			except TypeError:
				print('wrong number of parameters')

	def nick(self, _, nick):
		print('got NICK command')
		self.session = nick

	def user(self, conn, *args):
		print('got USER command')
		print(self.session, args[0])
		if self.session != args[0]:
			print('wrong user')
		else:
			print('User ' + self.session + ' connected')
			reply = Reply(self, {'nick': self.session, 'host': args[1]})
			message = reply.prefix + ' ' + Reply.codes['RPL_WELCOME'] + ' :' + reply.text + ' ' + reply.nick + '!' + reply.nick + '@' + reply.host
			conn.send(message.encode('ascii'))

	def quit(self, conn):
		conn.send('Bye!')
		conn.close()
		self.session = None

class Message(object):
	"""IRC Message.

	Examples:
	NICK amy
	WHOIS doctor
	MODE amy +o
	JOIN #tardis
	QUIT
	PRIVMSG rory :Hey Rory...
	PRIVMSG #cmsc23300 :Hello everybody
	QUIT :Done for the day, leaving
	:borja!borja@polaris.cs.uchicago.edu PRIVMSG #cmsc23300 :Hello everybody
	:doctor!doctor@baz.example.org QUIT :Done for the day, leaving
	"""
	def __init__(self, server, text):
		self.server = server
		self.text = text#[510:]+'\r\n'

class Reply(Message):
	"""Reply message.

	Examples:
	:irc.example.com 001 borja :Welcome to the Internet Relay Network borja!borja@polaris.cs.uchicago.edu
	:irc.example.com 433 * borja :Nickname is already in use.
	:irc.example.org 332 borja #cmsc23300 :A channel for CMSC 23300 students
	"""
	codes = {'RPL_WELCOME': '001'}

	def __init__(self, server, user):
		print(super(Reply, self))
		super(Reply, self).__init__(server, 'Welcome!')
		self.prefix = ':' + server.addr
		self.nick = user['nick']
		self.host = user['host']

if __name__ == '__main__':
	 
	server = Server()
	s = socket.socket()
	server.addr = socket.gethostname()
	port = int(sys.argv[1])
	s.bind((server.addr, port))
	s.listen(5)
	while True:
		conn, addr = s.accept()
		print('Connection from ' + str(addr))
		while True:
			message = conn.recv(1024).decode('ASCII')
			server.handle(message, conn)
		#conn.close()
