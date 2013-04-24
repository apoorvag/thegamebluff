'''
Created on Mar 25, 2013

@author: kavya
'''
from socket import *
import socket
import RequestMessage
import Message
import ResponseMessage
import MessagePasser
import time
import NodeIdentity
import ConnectionEstablishment.TCPSetup
#import ConnectionEstablishment.ServerHandler
import GameInit.initiation
import GameInit.User
import GameInit.cards
import PeerDiscovery.Message

try:
    import cPickle as pickle
except:
    import pickle

class UsrModule:
    ip_addr = None
    port = 0
    choice = 0
    
    def __init__(self):
        self.ip_addr = socket.gethostbyname(socket.gethostname())
        print "ip address= %s" % self.ip_addr
        self.port = int(raw_input("Enter your port number."))
        self.Initiator = False
        self.username = None
        
        self.UDPsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        self.UDPsock.bind((self.ip_addr, self.port))
        
        self.UDPsock.setblocking(False)
        
        self.choice = 0
        self.play = True
        
        self.mp = MessagePasser.MsgPasser()
        
        self.UDPsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.UDPsocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self.UDPsocket.bind(('', 0))
        
        self.UDPsocket1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.UDPsocket1.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.UDPsocket1.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self.UDPsocket1.bind(('', 9999))
        
        self.clientList = []
        self.respList = []
        self.connection = None
        self.idList = []
        
        self.myBuffer = []
        self.predBuffer = []
        self.succBuffer = []
        self.TableBuffer = []
        self.myNode = []
        self.predNode = []
        self.succNode = []
        self.ackArray = []
        
        self.bluffMsg = []
        self.sender_ip = None
        self.sender_port = None
        
      
def sendGameRequest(um, username):
    um.Initiator = True
    um.username = username
    dest_port = 9999
    requestMsg = RequestMessage.ReqMessage(um.ip_addr, um.ip_addr, int(um.port), 9999, "Request", 0, "B-REQ")
    um.mp.broadcastRequest(requestMsg, um.UDPsocket) #broadcast socket
    start = time.time()
    while (time.time() - start < 30):
        respMsg = None
        respMsg = um.mp.receiveResp(um.UDPsock) #this node's socket
        if(respMsg is not None) :
            if(respMsg.type != "Response") :
                respMsg = None
        if respMsg is None :
            continue
        else :
            nodeId = NodeIdentity.NodeID(respMsg.src, respMsg.src_port, None, respMsg.username)
            um.respList.append(nodeId)
           
    print "size of list: %d\n" % (len(um.respList))
    
    if (len(um.respList) == 0) :
        print "No players available. Try again? Y/N\n"
        trial = raw_input()
        if(trial == "Y") :
            um.play = True
            return um.play
        else :
            um.play = False
            return um.play
    else:
        um.respList.append(NodeIdentity.NodeID(um.ip_addr, um.port, None, um.username)) # appending itself to list
        um.UDPsock.close()
        um.UDPsocket.close()
        um.UDPsocket1.close()
        print "%d setting up tcp\n" % um.port
        conn = ConnectionEstablishment.TCPSetup.createConn(um.ip_addr, um.port, um)
        um.connection = conn
        removeList = []
        conn.startThreads(um.respList, um.Initiator, removeList)
        
        time.sleep(5)
        
        
        
        if len(removeList) > 0 :
            for r in um.respList :
                for rem in removeList :
                    if r.ip_addr == rem.ip_addr :
                        if r.port == rem.port :
                            um.respList.remove(r)
                            break
                        
        print "printing respList\n"                
        for r in um.respList :
            print r.ip_addr, " ", r.port, " ", r.username, "\n"
            
        if len(removeList) > 0 :
            for x in conn.client_list :
                for rem in removeList :
                    if x.ip == rem.ip_addr :
                        if x.portnum == rem.port :
                            conn.client_list.remove(x)
                            break   
            
                
       
        print "preparing to send IP List"
        um.clientList = conn.client_list  
        ipMsg = Message.Msg(um.ip_addr, int(um.port), "IPList", 0, um.respList)
        ipMsg_string = pickle.dumps(ipMsg) # sending list to other nodes
        
        for x in conn.client_list :
            
            x.cSock.sendall(ipMsg_string)
          
        print "sent IPList\n" 
                       
        time.sleep(10)
        
         
        gi = GameInit.initiation.Init(um.Initiator)
        print "generating ID list\n"
        gi.genId(um.respList)
        
        
        for node in um.respList :
            print node.ip_addr, " ", node.port, " ", node.id
        
        deadArray = []  
        idMsg = Message.Msg(um.ip_addr, int(um.port), "IDList", 0, um.respList)
        idMsg_string = pickle.dumps(idMsg) # sending list to other nodes
        print "SEnding idList to: \n"
        for x in conn.client_list :
            print x.ip, " ", x.portnum
            try :
                x.cSock.sendall(idMsg_string)
            except :
                print "Cannot send!!\n"
                n = NodeIdentity.NodeID(x.ip, x.portnum, None)
                deadArray.append(n)
        print "\n"
        
        time.sleep(5)
        
        #after sending list, check ackarray. Should have got response from all nodes.
        print "checking for dead nodes\n"
        flag = 0
        for id in um.respList :
            print id.ip_addr, " ", id.port, "\n"
            if id.ip_addr == um.ip_addr :
                if id.port == um.port :
                    print "excluding myself\n"
                    continue
            flag = 0
            for ack in um.ackArray :
                print "ack:  ", ack.src, " ", ack.src_port, "\n"  
                if ack.src == id.ip_addr :
                    if ack.src_port == id.port :
                        
                        flag = 1
                        break
            
            if flag == 0 :
                print "appending to dead array: ", id.ip_addr, " ", id.port, "\n"
                deadArray.append(id) # did not receive ack from this node
                
        
        #function to tell other nodes to remove id
        if len(deadArray) > 0 :
            
            #TODO: remove dead node from my list!
            for r in um.respList :
                for d in deadArray :
                    if r.ip_addr == d.ip_addr :
                        if r.port == d.port :
                            um.respList.remove(r)
                            break
                        
            for x in conn.client_list :
                for d in deadArray :
                    if x.ip == d.ip_addr :
                        if x.portnum == d.port :
                            conn.client_list.remove(x)
                            break   
            
            delMsg = PeerDiscovery.Message.Msg(um.ip_addr, um.port, "DELETE", 0, deadArray)
            delMsg_string = pickle.dumps(delMsg)
            for x in conn.client_list :
                x.cSock.sendall(delMsg_string)
        
        user1 = GameInit.User.user()
        user1.createBuffers(um.ip_addr, um.port, um.respList, um)
        
        '''ackList = []
        time.sleep(2)
        for sh in conn.server.shList :
            if len(sh.ackList) != 0:
                print "length of ackList not 0\n"
                ackList.append(sh.ackList[0])
            else:
                print "Waiting on Acks"
            
        check = gi.checkAck(um.respList, ackList, 1, int(um.port))
        if check == False :
            print "checkAck false\n"
            time.sleep(2)
            
            ackList = []
            for sh in conn.server.shList :
                ackList.append(sh.ackList[0])
                
            check = gi.checkAck(um.respList, ackList, 2, int(um.port))
            
            if check == False :
                print"Can't Proceed. Check=false\n"'''
                
                
                
            
        #if check == True : # all ACK's have been received
            #print "checkAck true"
        start = False
        if um.respList[0].ip_addr == um.ip_addr :
            if um.respList[0].port == um.port :
                print "start=True I need to start"
                start = True
              
            #cards = GameInit.cards.cards_init(respList)  
            #cards.gen_cards()  
            print "*\n*\n*\n*\n*\n*\n*\n*\n*\nGenerating Token!!!\n"
            ini = GameInit.initiation.Init(um.Initiator)
            tokenCards = ini.StartInitiation(um.respList) 
            
            success = False
            while success == False :
                if len(um.respList) == 1 : # all other nodes dead
                    break
                    
                if start == False :
                    print "if start=false..create token msg\n"
                    tokenMsg = Message.Msg(um.ip_addr, int(um.port), "TOKEN", 0, tokenCards)
                    tokenMsg_string = pickle.dumps(tokenMsg) # sending list to other nodes
                    for x in conn.client_list :
                        if x.ip == um.respList[0].ip_addr :
                            if x.portnum == um.respList[0].port :
                                print "sending token to ", um.respList[0].port, "\n"
                                try :
                                    x.cSock.sendall(tokenMsg_string)
                                    success = True
                                except :
                                    print um.respList[0].ip_addr, " ", um.respList[0].port, " has crashed."
                                    rem_node = um.respList[0]
                                    for r in um.respList :
                                        if r.ip_addr == um.respList[0].ip_addr :
                                            if r.port == um.respList[0].port :
                                                um.respList.remove(r)
                                                break
                            
                                    for x in conn.client_list :
                                        if x.ip == um.respList[0].ip_addr  :
                                            if x.portnum == um.respList[0].port :
                                                conn.client_list.remove(x)
                                                break   
                                    deadArray = []
                                    deadArray.append(rem_node)
                                    delMsg = PeerDiscovery.Message.Msg(um.ip_addr, um.port, "DELETE", 0, deadArray)
                                    delMsg_string = pickle.dumps(delMsg)
                                    for x in conn.client_list :
                                        x.cSock.sendall(delMsg_string) #TODO: all sends need to be tested
                                        
                                    user1 = GameInit.User.user()
                                    user1.createBuffers(um.ip_addr, um.port, um.respList, um)
                                    ini = GameInit.initiation.Init(um.Initiator)
                                    tokenCards = ini.StartInitiation(um.respList) 
                                    if um.respList[0].ip_addr == um.ip_addr :
                                        if um.respList[0].port == um.port :
                                            print "start=True I need to start"
                                            start = True
                                
                            
                else :
                    print "My cards: \n"
                    for c in tokenCards.cards :
                        print c, " "
                    print "\n"
                    playerList = []
                    playerList.append(um.username)
            
                    for c in conn.client_list :
                        if c.ip == um.ip_addr :
                            if c.portnum == um.port :
                                playerList.append(c.username)

                    for c in conn.client_list :
                        if c.ip != um.ip_addr :
                            if c.portnum != um.ip_addr :
                                playerList.append(c.username)
                                
                    tokenMsg = Message.Msg(um.ip_addr, int(um.port), "TOKEN", 0, tokenCards)
                    gu = GameInit.User.user()
                    success = gu.passToken(um.ip_addr, int(um.port), tokenMsg, conn.client_list, um, playerList)
                    if success == False :
                        print um.succNode.ip_addr, " ", um.succNode.port, " has crashed."
                        rem_node = um.succNode
                        for r in um.respList :
                            if r.ip_addr == um.succNode.ip_addr :
                                if r.port == um.succNode.port :
                                    um.respList.remove(r)
                                    break
                            
                        for x in conn.client_list :
                            if x.ip == um.succNode.ip_addr  :
                                if x.portnum == um.succNode.port :
                                    conn.client_list.remove(x)
                                    break   
                        deadArray = []
                        deadArray.append(rem_node)
                        delMsg = PeerDiscovery.Message.Msg(um.ip_addr, um.port, "DELETE", 0, deadArray)
                        delMsg_string = pickle.dumps(delMsg)
                        for x in conn.client_list :
                            x.cSock.sendall(delMsg_string)
                                        
                        user1 = GameInit.User.user()
                        user1.createBuffers(um.ip_addr, um.port, um.respList, um)
                        ini = GameInit.initiation.Init(um.Initiator)
                        tokenCards = ini.StartInitiation(um.respList) 
                        if um.respList[0].ip_addr == um.ip_addr :
                            if um.respList[0].port == um.port :
                                print "start=True I need to start"
                                start = True
            if success == False :
                print "All players have crashed!!"
                return False                
            
        
                
            
def acceptGameRequest(um, username):
    requestMsg = None
    um.username = username
    start = time.time()
    while (time.time() - start < 10):
        requestMsg = um.mp.receiveBroadcast(um.UDPsocket1) #broadcast socket
        if (requestMsg is not None) :
            break
        
    if requestMsg is None :
        print "No outstanding requests. Try again? Y/N\n"
        trial = raw_input()
        if(trial == "Y") :
            um.play = True
            return um.play
        else :
            um.play = False
            return um.play
        
    else :
        print "Request Object received \n"
        print "src: %s, dest: %s, src_port: %d, dest_port: %d, timestamp: %d, data: %s, type: %s" % (requestMsg.src, requestMsg.dest, requestMsg.src_port, requestMsg.dest_port, requestMsg.timestamp, requestMsg.data, requestMsg.type)
        response1 = ResponseMessage.RespMessage(um.ip_addr, um.username, requestMsg.src, int(um.port), int(requestMsg.src_port), "Response", 0, "YaayRESP")
        um.mp.sendResponse(response1, um.UDPsock) # my socket
        print "sent response"
        
        start = time.time()
        while (time.time() - start < 10) :
            ackMsg = um.mp.receiveBroadcast(um.UDPsock)
            if (ackMsg is not None) :
                break
        if ackMsg is None :
            print "No outstanding requests. Try again? Y/N\n"
            trial = raw_input()
            if(trial == "Y") :
                um.play = True
                return um.play
            else :
                um.play = False
                return um.play
        
            
        um.UDPsock.close()
        um.UDPsocket.close()
        um.UDPsocket1.close()
        print "%d setting up tcp\n" % um.port
        conn1 = ConnectionEstablishment.TCPSetup.createConn(um.ip_addr, um.port, um)
        um.connection = conn1
        removeList = []
        flag = conn1.startServerThread(requestMsg.src, int(requestMsg.src_port), um.Initiator)
       
        if flag == False :
            print "can't proceed!!!\n"
            return False
        
        
        my_server = None
        nodeList = []
        
        for x in conn1.server_list:
                    print "check"
                    my_server = x
                    nodeList = x.data_list.data
                    
        conn1.startOtherThreads(nodeList, requestMsg.src, int(requestMsg.src_port), my_server, removeList)
        
        time.sleep(5)
        
        if len(removeList) > 0 :
            for n in nodeList :
                for rem in removeList :
                    if n.ip_addr == rem.ip_addr :
                        if n.port == rem.port :
                            nodeList.remove(n)
                            break
        print "printing nodeList\n"                
        for n in nodeList :
            print n.ip_addr, " ", n.port, " ", n.username, "\n"
            
        if len(removeList) > 0 :
            for x in conn1.client_list :
                for rem in removeList :
                    if x.ip == rem.ip_addr :
                        if x.portnum == rem.port :
                            conn1.client_list.remove(x)
                            break   
        
        um.clientList = conn1.client_list  
        
        time.sleep(10)
        
        if len(um.idList) == 0 :
            print "Requester crashed. Somebody take over.\n"

    