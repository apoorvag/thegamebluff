'''
Created on Mar 25, 2013

@author: kavya
'''

class ReqMessage:
    '''
    classdocs
    '''
    src = None
    dest = None
    src_port = 0
    dest_port = 0
    type = None
    timestamp = 0
    data = None


    def __init__(self, src, dest, src_port, dest_port, type, timestamp, data):
        '''
        Constructor
        '''
        self.src = src
        self.dest = dest
        self.src_port = src_port
        self.dest_port = dest_port
        self.type = type
        self.timestamp = timestamp
        self.data = data
        
    def __repr__(self):
        
        return '<%s %s %d %d %s %d %s>' % (self.src, self.dest, self.src_port, self.dest_port, self.type, self.timestamp, self.data)
        
    @property
    def src(self):
        return self._src
    
    @property
    def dest(self):
        return self._dest
    
    @property
    def src_port(self):
        return self._src_port
    
    @property
    def dest_port(self):
        return self._dest_port
    
    @property
    def type(self):
        return self._type
    
    @property
    def timestamp(self):
        return self._timestamp
    
    @property
    def data(self):
        return self._data
    
    
        
        
