'''
Created on Mar 27, 2013

@author: kavya
'''
import socket
import threading
import time
import errno
from multiprocessing import TimeoutError

try:
    import cPickle as pickle
except:
    import pickle
#import Client
import ServerHandler

class server(threading.Thread):
    def __init__(self, ip, port, clientList, Initiator, um):
        super(server, self).__init__()
        self.ip = ip
        self.port = port
        #self.client = client
        self.TCPsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.TCPsock.bind((ip, port)) 
        self.cl = clientList
        self.Initiator = Initiator
        self.shList = []
        self.um = um
        
    def run(self):
        while True:
            self.TCPsock.settimeout(None)
            
            self.TCPsock.listen(1)
            try :
                conn, addr = self.TCPsock.accept()
            except :
                print "exception thrown!in server run\n"
                return False
            
            sh = ServerHandler.sHandler(conn, self.ip, self.port, self.cl, self.Initiator, self.um)
            self.shList.append(sh)
            sh.start()
            
class server1(threading.Thread):
    def __init__(self, ip, port, clientList, Initiator, um):
        super(server1, self).__init__()
        self.ip = ip
        self.port = port
        self.TCPsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.TCPsock.bind((ip, port)) 
        #self.TCPsock.setblocking(False)
        
        self.cl = clientList
        self.Initiator = Initiator
        self.data_list = []
        self.shList = []
        self.um = um
        
    def connWait(self, TCPsock):
        
            TCPsock.settimeout(50.0)
            TCPsock.listen(1)
            try :
                conn, addr = TCPsock.accept()
            except :
                print "Terminating game.."
                return False
            
            if conn is None :
                print "requester has shut down. Terminating game.."
                return False
            
            print "printing connection: ", conn, "\n"
                
            data_string = None
            start = time.time()
            while time.time() - start < 50 :
                if data_string is not None :
                    break
                try :
                    data_string = conn.recv(1024)
                except IOError as e:
                    if e.errno == errno.EWOULDBLOCK:
                        data_string = None
                        
            if data_string is None :
                print "Terminating Game!no data_string\n"
                return False
                    
            self.data_list = pickle.loads(data_string)
            ipList = []
            print "in server--type: ", self.data_list.type
            if self.data_list.type == "IPList" :
                print "in server..\n"
                for x in self.data_list.data:
                    print "ip: "
                    print x.ip_addr
                    print "\tport: "
                    print x.port
                    print "\td: "
                    print x.id
                    print "\n"
                    
            sh = ServerHandler.sHandler(conn, self.ip, self.port, self.cl, self.Initiator, self.um)
            self.shList.append(sh)
            sh.start()
            return True
            
    def run(self):
        while True:
            self.TCPsock.settimeout(None)
            self.TCPsock.listen(1)
            try :
                conn, addr = self.TCPsock.accept()
            except :
                print "Exception thrown!In server1 run\n"
                return False
            sh = ServerHandler.sHandler(conn, self.ip, self.port, self.cl, self.Initiator, self.um)
            self.shList.append(sh)
            sh.start()
        
