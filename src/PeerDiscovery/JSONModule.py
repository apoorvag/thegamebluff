'''
Created on Mar 25, 2013

@author: kavya
'''
import json

class MyEncoder(json.JSONEncoder):
    
    def default(self, o):
        #o = super(MyEncoder, self).default(o)
        #return json.JSONEncoder.encode(self, o)
        return o.__dict__
    
    

class MyDecoder(json.JSONDecoder):
    
    def default(self, json_string):
        return json.JSONDecoder.decode(self, json_string)