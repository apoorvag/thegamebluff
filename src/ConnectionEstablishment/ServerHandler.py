'''
Created on Mar 31, 2013

@author: kavya
'''
import threading
import os
try:
    import cPickle as pickle
except:
    import pickle
    
import socket
import GameInit.User
import UI.UI_game
import PeerDiscovery.Message
import time
import errno
import GamePlay.rules
#import PeerDiscovery.UserModule


class sHandler(threading.Thread):
    def __init__(self, conn, my_ip, my_port, clientList, Initiator, um):
        super(sHandler, self).__init__()
        self.conn = conn
        self.my_ip = my_ip
        self.my_port = my_port
        self.username = um.username
        self.cl = clientList
        self.Initiator = Initiator
        self.ackList = []
        self.um = um
        
        
        
    def run(self):
        u = GameInit.User.user()
        while True:
            data_string = None
            while data_string is None :
                try :
                    data_string = self.conn.recv(2048)
                except IOError as e:
                    if e.errno == errno.EWOULDBLOCK:
                        data_string = None
            self.data = pickle.loads(data_string) #msg that is being received
            print "In server handler_type",self.data.type

             # modified : retrieve cardonTable from um.tableBuffer
            cardsOnTable = []
            # modified : retrieve playerList: first=myself, second=cur player
            playerList = []
            playerList.append(self.username)
            
            for c in self.cl :
                if c.ip == self.data.src :
                    if c.portnum == self.data.src_port :
                        playerList.append(c.username)

            for c in self.cl :
                if c.ip != self.data.src :
                    if c.portnum != self.data.src_port :
                        playerList.append(c.username)
                    
            print "type: ", self.data.type
            if self.data.type == "IDList" :
                self.um.idList = self.data.data
                for id in self.um.idList :
                    print id.ip_addr, " ", id.port, " ", id.id
                    
                for x in self.um.clientList :
                    if x.portnum == self.data.src_port :
                        if x.ip == self.data.src :
                            print "sending ack for idList\n"
                            ackMsg = PeerDiscovery.Message.Msg(self.my_ip, int(self.my_port), "ACK", 0, "IDlist received")
                            ackMsgString = pickle.dumps(ackMsg)
                            x.cSock.sendall(ackMsgString)
                    
                    
                '''check = False
                while check == False :
                    
                    counter = 0
                    for ack in self.um.ackArray :
                        for id in idList :
                            if ack.src == id.ip_addr :
                                if ack.src_port == id.port :
                                    print "printing ack details:\n"
                                    print ack.src, " ", ack.src_port
                                    counter = counter + 1
                                    
                    if counter == len(idList) - 2 :
                        print "check=True. can deliver idList"
                        check = True
                        self.um.ackarray = []
                    else :
                        time.sleep(2)'''
                    
                u.receiveMsg(self.my_ip, self.my_port, self.data, self.cl, self.Initiator, self.um)
            
            elif self.data.type == "ACK" :
                print "receiving acks \n"
                self.um.ackArray.append(self.data)
                
                
            elif self.data.type ==  "ACK1" :
                self.ackList.append(self.data.data)
                   
            
            elif self.data.type == "DELETE" :
                print "DELETE msg received\n"
                print "delete list :\n"
                for node in self.data.data :
                    print node.ip_addr, " ", node.port, " ", node.id, "\n"
                    for x in self.um.respList :
                        if x.ip == node.ip_addr :
                            if x.portnum == node.port :
                                self.um.respList.remove(x)
                    for x in self.um.clientList :
                        #kill thread.
                        if x.ip == node.ip_addr :
                            if x.portnum == node.port :
                                self.um.clientList.remove(x)
                                
                                
                
            elif self.data.type == "TOKEN" :
                print "token received\n"
                #token_count = token_count + 1
                #if token_count == 2 :
                    #print "The following cards will be discarded: \n"
                    #for c in self.data.data.cards :
                     #   print c, " "
                    #print "\n"
                    #return
                #else :
                print "Token Received from %s:%d " % (self.data.src, self.data.src_port)
                #u = GameInit.User.user()
                success = u.passToken(self.my_ip, self.my_port, self.data, self.cl, self.um, playerList)
                start = True
                while success == False :
                    
                    if start == True :
                        print self.um.succNode.ip_addr, " ", self.um.succNode.port, " has crashed."
                        rem_node = self.um.succNode
                        
                    else :
                        print self.um.respList[0].ip_addr, " ", self.um.respList[0].port, " has crashed."
                        rem_node = self.um.respList[0]
                        
                        
                    for r in self.um.respList :
                        if r.ip_addr == rem_node.ip_addr :
                            if r.port == rem_node.port :
                                self.um.respList.remove(r)
                                break
                        
                    for x in self.conn.client_list :
                        if x.ip == rem_node.ip_addr  :
                            if x.portnum == rem_node.port :
                                self.conn.client_list.remove(x)
                                break  
                             
                    deadArray = []
                    deadArray.append(rem_node)
                    delMsg = PeerDiscovery.Message.Msg(self.um.ip_addr, self.um.port, "DELETE", 0, deadArray)
                    delMsg_string = pickle.dumps(delMsg)
                    for x in self.conn.client_list :
                        x.cSock.sendall(delMsg_string) #TODO: test all sends
                    
                    u = GameInit.User.user()
                    u.createBuffers(self.um.ip_addr, self.um.port, self.um.respList, self.um)
                    ini = GameInit.initiation.Init(self.um.Initiator)
                    tokenCards = ini.StartInitiation(self.um.respList) 
                    if self.um.respList[0].ip_addr == self.um.ip_addr :
                        if self.um.respList[0].port == self.um.port :
                            print "start=True I need to start"
                            start = True
                        else :
                            start = False
                    tokenMsg = PeerDiscovery.Message.Msg(self.um.ip_addr, int(self.um.port), "TOKEN", 0, tokenCards)
                    #tokenMsg_string = pickle.dumps(tokenMsg) # sending list to other nodes
                    if start == True :
                        success = u.passToken(self.my_ip, self.my_port, tokenMsg, self.cl, self.um)
                    else :
                        tokenMsg_string = pickle.dumps(tokenMsg) # sending list to other nodes
                        for x in self.conn.client_list :
                            if x.ip == self.um.respList[0].ip_addr :
                                if x.portnum == self.um.respList[0].port :
                                    print "sending token to ", self.um.respList[0].port, "\n"
                                    try :
                                        x.cSock.sendall(tokenMsg_string)
                                        success = True
                                    except :
                                        success = False
                                        
            # Handle PlayToken
            elif self.data.type == "PlayToken":
                #this token means its time to make my move
                game = GamePlay.rules.Play()
                game.MyTurnPlay(self.my_ip,self.my_port,self.cl)
            
            # Handle Announcement Message:
            elif self.data.type == "ANNOUNCEMENT":
                print "Announcement received from %s:%d \n" % (self.data.src, self.data.src_port)
                playerName = None
                for c in self.cl :
                    if c.ip == self.data.src :
                        if c.portnum == self.data.src_port :
                            playerName = c.username
                            
                announcement = playerName + "'s turn to play!"
                # Show who is playing in red on screen
                print announcement
                #gui = UI.UI_game.GameUI(self.um, self.um.myBuffer.cardList, cardsOnTable, playerList, False, False, None, announcement)
                #gui.start()
                self.gui.info = announcement
                #self.gui.update_screen()
                self.gui.display_screen()
                
                
            # Handle Claim Message:
            elif self.data.type == "CLAIM":
                print "Claim msg received from %s:%d \n" % (self.data.src, self.data.src_port)
                self.um.sender_ip = self.data.src
                self.um.sender_port = self.data.src_port
                self.claimCards = self.data.data[0] #TODO: what???
                self.um.TableBuffer.append(self.data.data[1])
                print "table buffer contents:\n"
                for t in self.um.TableBuffer :
                    print t, " "
                print "\n"
                
                # Enable Callbluff button 
                no_cards = str(self.claimCards[0])
                type_cards = self.claimCards[1]
                cards = no_cards + " " + type_cards
                
                for c in self.cl :
                    if c.ip == self.data.src :
                        if c.portnum == self.data.src_port :
                            playerName = c.username
                            
                announcement = playerName + " claims to have placed " + cards + " on table\n"
                #gui = UI.UI_game.GameUI(self.um, self.um.myBuffer.cardList, self.data.data[1], playerList, False, True, None, announcement) #TODO: what??
                #gui.update_screen()
                #gui.start()
                for c in self.data.data[1] :
                    c += '.jpg'
                    self.gui.new_cards.append(os.path.join(self.gui.picpath, c)) #TODO: append/new list?
                
                print "printing new_card:\n"
                for nc in self.gui.new_cards :
                    print nc, " "
                print "\n"
                
                self.gui.call_bluff = True
                self.gui.info = announcement
                self.gui.update_screen()
                self.gui.display_screen()
            
            # Handle Announcement of CallBluff Message:  
            elif self.data.type == "ANNOUNCE_BLUFF":
                print "Announce Bluff msg received from %s:%d \n" % (self.data.src, self.data.src_port)
                callbluffer_id = self.data.data
                print "callbluffer_id: ", callbluffer_id, "\n"
                un = None
                print "len = ", len(self.um.respList)
                for r in self.um.respList :
                    print "r id = ", r.id, "\n"
                    if r.id == int(callbluffer_id) :
                        print "match\n"
                        un = r.username
                print "un= ", un  
                announcement = str(un) + " has called bluff!"
                self.gui.info = announcement
                self.your_turn = False
                self.call_bluff = False
                self.call_bluff_user = un
                self.gui.display_screen()
                # Disable Callbluff button
                #gui = UI.UI_game.GameUI(self.um, self.um.myBuffer.cardList, cardsOnTable, playerList,False, False, callbluffer, None)
                #gui.update_screen()
                #gui.start()
            
            # Handle CallBluff Message:
            elif self.data.type == "BLUFF":
                print "Bluff msg received from %s:%d \n" % (self.data.src, self.data.src_port)
                self.um.bluffMsg.append(self.data)
                       
                # Broadcast "AnnounceCallBluff" msg
                        
                    
            elif self.data.type == "OPENDECK" :
                print "open deck msg received\n"
                if len(self.data.data) > 0 :
                    print "The following cards will be discarded: \n"
                    for c in self.data.data:
                        print c, " "
                    print "\n"
                new_cards = [] 
                self.gui = UI.UI_game.GameUI(self.um, self.um.myBuffer.cardList, cardsOnTable, playerList, False, False, None, None)
                #gui.update_screen()
                self.gui.start()
                
                    
            else :
                print self.data.data
    
    
 