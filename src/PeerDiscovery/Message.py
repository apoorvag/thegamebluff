'''
Created on Apr 1, 2013

@author: kavya
'''

class Msg:
    '''
    classdocs
    '''
    src = None
    src_port = 0
    type = None
    timestamp = 0
    data = None

    def __init__(self, src, src_port, type, timestamp, data):
        '''
        Constructor
        '''
        self.src = src
        self.src_port = src_port
        self.type = type
        self.timestamp = timestamp
        self.data = data
        
    #def __repr__(self):
        
     #   return '<%s %d %d %s %d %s>' % (self.src, self.dest, self.src_port, self.dest_port, self.type, self.timestamp, self.data)
        
    @property
    def src(self):
        return self._src
    
    
    @property
    def src_port(self):
        return self._src_port
    
    
    @property
    def type(self):
        return self._type
    
    @property
    def timestamp(self):
        return self._timestamp
    
    @property
    def data(self):
        return self._data
    
    
        
        
