'''
Created on Mar 26, 2013

@author: kavya
'''
class NodeID:
    def __init__(self, ip_addr, port, id, username):
        self.ip_addr = ip_addr
        self.port = int(port)
        self.id = id
        self.username = username
        
    @property
    def ip_addr(self):
        return self._ip_addr
    
    @property
    def port(self):
        return self._port
    
    @property
    def id(self):
        return self._id
    
    
    @property
    def username(self):
        return self._username
    
    