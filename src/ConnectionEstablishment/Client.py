'''
Created on Mar 26, 2013

@author: kavya
'''
import threading
import socket
#import PeerDiscovery.MessagePasser
import PeerDiscovery.NodeIdentity

class client(threading.Thread):
    def __init__(self, ip_addr, port, username, removeList):
        super(client, self).__init__()
        self.ip = ip_addr
        self.portnum = port
        self.username = username
        self.cSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.removeList = removeList
        
    def run(self):
        flag = 0
        try :
            self.cSock.connect((self.ip, self.portnum))
        except Exception, e :
            flag = 1
            nodeId = PeerDiscovery.NodeIdentity.NodeID(self.ip, self.portnum, None)
            self.removeList.append(nodeId)
            print "Something wrong with %s:%d. Exception type is %s\n" % (self.ip, self.portnum, e)
            
        
        if flag == 0 :
            print "connected with %s and %d \n" % (self.ip, self.portnum)
        
