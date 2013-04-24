'''
Created on Mar 25, 2013

@author: kavya
'''
#import UserModule
from socket import *
import errno
import socket
try:
    import cPickle as pickle
except:
    import pickle
import Message


class MsgPasser():
    def __init__(self):
        print "in self"
        
    def broadcastRequest(self, reqObject, UDPsocket):
        obj_string = pickle.dumps(reqObject)
        UDPsocket.sendto(obj_string, ('255.255.255.255', 9999))
        
    
    def receiveBroadcast(self, UDPsocket1):
        msg = None
        try:
            (msg, addr) = UDPsocket1.recvfrom(1024)
        except IOError as e:
            if e.errno == errno.EWOULDBLOCK:
                msg = None
                return msg
        if msg is not None :
            req = pickle.loads(msg)
            msg1 = req
        else :
            msg1 = None
            
        return msg1
        
    def sendBroadcast(self, reqObject, UDPsock):
        #print "Request Object"
        #print "src: %s, dest: %s, src_port: %d, dest_port: %d, timestamp: %d, data: %s, type: %s" % (reqObject.src, reqObject.dest, reqObject.src_port, reqObject.dest_port, reqObject.timestamp, reqObject.data, reqObject.type)
        obj_string = pickle.dumps(reqObject)
        #print "request after dumping: \n", obj_string
        UDPsock.sendto(obj_string, (reqObject.dest, reqObject.dest_port))
        
    def receiveResp(self, UDPsock):
        msg1 = None
        req = None
        try:
            (msg, addr) = UDPsock.recvfrom(1024)
        except IOError as e:
            if e.errno == errno.EWOULDBLOCK:
                msg = None
                return msg
        
        if (msg is not None) :
            
            req = pickle.loads(msg)
            ack_msg = Message.Msg(req.dest, req.dest_port, "ACK", 0, "UDP ACK")
            ack_string = pickle.dumps(ack_msg)
            UDPsock.sendto(ack_string, (req.src, req.src_port))
            print "sent ACK for response!"
            #print "request after loads: \n", req
            msg1 = req
        else :
            msg1 = None
        return msg1
    
    def receiveReq(self, UDPsock):
        msg1 = None
        req = None
        try:
            (msg, addr) = UDPsock.recvfrom(1024)
        except IOError as e:
            if e.errno == errno.EWOULDBLOCK:
                msg = None
                return msg
        print "after recvfrom: \n", msg
        
        if (msg is not None) :
            req = pickle.loads(msg)
            #print "request after loads: \n", req
            msg1 = req
        else :
            msg1 = None
        return msg1
        
        
    def sendResponse(self, respObject, UDPsock):
        #print "Response Object"
        #print "src: %s, dest: %s, src_port: %d, dest_port: %d, timestamp: %d, data: %s, type: %s" % (respObject.src, respObject.dest, respObject.src_port, respObject.dest_port, respObject.timestamp, respObject.data, respObject.type) 
        obj_string1 = pickle.dumps(respObject)
        UDPsock.sendto(obj_string1, (respObject.dest, respObject.dest_port))
        
    def sendMessage(self, cList, option):
        if(option == 1) :
            check = 4700
        else:
            if(option == 2) :
                check = 4701
            else:
                if(option == 3) :
                    check = 4702
        
        for x in cList:
            if(x.portnum == check) :
                print "sending hey to %d \n" % x.portnum
                x.cSock.sendall("hey")
                
    def sendMsg(self, ip, port, msg, cList) :
        
        msg_string = pickle.dumps(msg)
        for x in cList :
            if x.ip == ip :
                if x.portnum == port:
                    print "sending ACK to %d \n" % x.portnum
                    x.cSock.sendall(msg_string) 
            
        
        
        
        
        
    
        