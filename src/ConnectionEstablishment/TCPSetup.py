'''
Created on Mar 30, 2013

@author: kavya
'''
import Client
import Server

class createConn:
    def __init__(self, ip, port, um):
        self.ip = ip
        self.port = port
        self.client_list = []
        self.server = None
        self.server_list = []
        self.um = um
        
    def startThreads(self, nList, Initiator, removeList):
        
        s = Server.server(self.ip, self.port, self.client_list, Initiator, self.um)
        self.server = s
        s.start()
            
        i = 0
        for n in nList :
            if n.ip_addr == self.ip :
                if (n.port == self.port) : # change 
                    continue
            c = Client.client(n.ip_addr, n.port, n.username, removeList)
            self.client_list.append(c)
            self.client_list[i].start()
            i = i + 1 
            
    def startServerThread(self, source_ip, source_port, Initiator):
        s = Server.server1(self.ip, self.port, self.client_list, Initiator, self.um)
        self.server = s
        flag = s.connWait(s.TCPsock)
        if flag == False :
            return False
        self.server_list.append(s)
        return True
        
    def startOtherThreads(self, nodeList, source_ip, source_port, my_server, removeList):
        my_server.start()
        
        i = 0
        for n in nodeList :
            if n.ip_addr == self.ip :
                if (n.port == self.port) : # change 
                    continue
            c = Client.client(n.ip_addr, n.port, n.username, removeList)
            self.client_list.append(c)
            self.client_list[i].start()
            i = i + 1 
            
        
        
        
    
        
        
        