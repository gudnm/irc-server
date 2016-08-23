import socket
import sys
import pdb

class IRC:
    """Handle all the IRC protocol logic."""
    def __init__(self):
        self.commands = {'QUIT': self.quit, 'NICK': self.nick, 'USER': self.user}

    def handle(self, message):
        messageparts = message.split()
        command, args = messageparts[0], messageparts[1:]
        if command in self.commands:
            print(args)
            self.commands[command](args)

    def handle_outcoming(self):
        pass

    def nick(self, messageparts):
        print('got NICK command')
        self.session = messageparts[0]

    def user(self, args):
        print('got USER command')
#        print(self.session, args[0])
        if self.session != args[0]:
            print('wrong user')
        else:
            print('User ' + self.session + ' connected')
            reply = Reply(self, {'nick': self.session, 'host': args[1]})


    def quit(self, args=None):
        print('got QUIT command')
        conn.send('Bye!'.encode('ascii'))
        conn.close()
        self.session = None


class Server:
    """Handle sockets."""
    def __init__(self, irc, port):
        self.addr = None
        self.session = None
        self.irc = irc
        self.conn = None
        self.port = port

    def run(self):
        s = socket.socket()
        self.addr = socket.gethostname()

        s.bind((self.addr, self.port))
        s.listen(5)
        while True:
            conn, addr = s.accept()
            print('connection from ' + str(addr))
            while True:
                try:
                    message = conn.recv(1024).decode('ASCII')
                    self.irc.handle(message)
                except OSError:
                    print("connection closed")
                    break

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

    def format(self):
        message = (reply.prefix + ' ' + Reply.codes['RPL_WELCOME'] 
                   + ' :' + reply.text + ' ' + reply.nick + '!' 
                   + reply.nick + '@' + reply.host)
        
        #conn.send(message.encode('ascii'))

if __name__ == '__main__': 
    irc = IRC()  
    port = int(sys.argv[1])
    server = Server(irc, port)
    server.run()
