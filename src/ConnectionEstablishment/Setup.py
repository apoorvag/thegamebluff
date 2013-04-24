'''
Created on Mar 26, 2013

@author: kavya
'''
import socket
import Client
import Server
import PeerDiscovery.MessagePasser

try:
    import cPickle as pickle
except:
    import pickle

class TCPSetup:
    def __init__(self, ip_addr, port, nodeList):
        self.TCPsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.TCPsock.bind((ip_addr, port))
        self.client_list = []
        #self.connectedList =[]
        
        i = 0
        for x in nodeList:
            if (x.port == port) : 
                continue
            
            #c = Client.client(x.ip_addr, x.port, self.connectedList)
            c = Client.client(x.ip_addr, x.port)
            self.client_list.append(c)
            self.client_list[i].start()
            i = i + 1
        
        #separate this    
        #self.TCPsock.listen(1)
        #conn, addr = self.TCPsock.accept()
        #print "server accepted connection from ...\n" 
        #data = conn.recv(1024)
        #print data
        #while True:
            #msg = conn.recv(1024)
            #print msg
        #till here     
        
class RespTCPSetup:
    def __init__(self, ip_addr, port):
        self.TCPsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.TCPsock.bind((ip_addr, port))
        self.node_list = []
        self.clients = []
        #self.connectedList =[]
        self.TCPsock.listen(1)
        conn, addr = self.TCPsock.accept()
        print "server accepted connection from ..\n"
        data_string = conn.recv(1024)
        data = pickle.loads(data_string)
        self.node_list = data
        print "printing list: \n"
        for x in self.node_list:
            print "ip:"
            print x.ip_addr
            print "\t"
            print "Port:"
            print x.port
            print "\n"
        i = 0
        for x in self.node_list:
            if (x.port == port) :
                continue
            
            #c = Client.client(x.ip_addr, x.port, self.connectedList)
            c = Client.client(x.ip_addr, x.port)
            self.clients.append(c)
            self.clients[i].start()
            i = i + 1
        
        #separate this
        #while True:
            #msg = conn.recv(1024)
            #print msg 
        #till here   
        #s = Server.server1(self.TCPsock)
        #s.start()
            
        #for y in self.node_list:
            #if(y.port == port) :
                #continue
            
            #s = Server.server1(self.TCPsock)
            #s.start()
            
            
        