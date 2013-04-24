import os, sys
import pygame
import threading
from pygame.locals import *
import wx
import PeerDiscovery.Message
try:
    import cPickle as pickle
except:
    import pickle
import time


class ClaimBox(wx.Frame):
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, 'Claim card', size=(300,200))
        panel = wx.Panel(self)
        
        myList = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
        claim = wx.ListBox(panel, -1, (20,20), (80,60), myList, wx.LB_SINGLE)
        claim.SetSelection(3)
        
class GameUI(threading.Thread):
    
    def __init__(self, um, my_cards_in, new_cards_in, player_list, your_turn_enable, call_bluff_enable, call_bluff_user, announcement_string): 
        """cards and table"""
        """in player list, first is your self, next is the player who take turn"""
        super(GameUI, self).__init__()
        print "****in init****\n"
        self.um = um
        
        self.my_cards_in = my_cards_in
        self.my_cardNo = len(my_cards_in)
        self.player_list = player_list
        self.your_turn = your_turn_enable
        self.call_bluff = call_bluff_enable
        self.call_bluff_user = call_bluff_user
        self.info = announcement_string
        
        self.remain_cards = my_cards_in
        self.out_cards = []
        
        """select pictures"""    
        tablecloth = "table1.jpg"
        cardarea = "cardarea.jpg"
        cardback = "cardback.jpg"
        
        """get all pictures"""
        self.picpath = os.getcwd() + "\pictures"
        self.table = os.path.join(self.picpath, tablecloth)
        self.card_area = os.path.join(self.picpath, cardarea)
        self.card_back = os.path.join(self.picpath, cardback)
        
        """card size & table size"""        
        self.table_size = (1500, 800)
        self.cardarea_size = (800, 150)
        self.card_size = (80, 100)
        self.redcross_size = (20, 20)
        self.claim_card_font_size = 25
        self.claim_mark_size = 30
        self.call_bluff_size = 30
        self.call_bluff_user_size = 30
        self.claim_card_size = (self.claim_card_font_size, self.claim_card_font_size)
        self.my_card_init_pos = (100, self.table_size[1] - 120)
        self.new_card_init_pos = (100, self.table_size[1] / 3) 
        self.cardarea_init_pos = (self.table_size[0]/4, self.table_size[1]/3)
        self.plyerlist_init_pos = (10, 0)
        self.me_player_pos = (600, 10)
        self.claim_cards_init_pos = (1450, 30)
        self.claim_mark_init_pos = (600, 420)
        self.call_bluff_init_pos = (600, 420)
        self.call_bluff_str = "CALL BLUFF"
        self.call_bluff_user_init_pos = (600,200)
        self.info_init_pos = (600, 50)
        self.info_size = 25
        
        """put card pic names into a list"""
        self.my_cards = []
        self.new_cards = []
        for card in my_cards_in:
            card += '.jpg'
            self.my_cards.append(os.path.join(self.picpath, card))
        
        for card in new_cards_in:
            card += '.jpg'
            self.new_cards.append(os.path.join(self.picpath, card))
        
        self.redcross = os.path.join(self.picpath, 'redcross.jpg')
            
        """show GameUI"""
        #self.show_table(self.my_cards, self.new_cards)
        
        self.screen = None
        self.background = None
        self.cardarea = None
        self.cardback = None
        self.redcrosspic = None
        self.my_cardpics = []
        self.redcross_flag = []
        self.new_cardpics = []
        self.claim_cards = []
        self.card_pos = dict()
        self.claim_card_pos = dict()
        self.me = None
        self.nextp = None
        self.claim_id = None
        print "****init done!!****\n"
        
    def run(self): 
        print "****inside run****\n"
        self.update_screen()
        print "****return from update screen****\n"
        print "before display screen\n"       
        self.display_screen()
        time.sleep(10)
        if self.your_turn == True :
            myTurn = PeerDiscovery.Message.Msg(self.um.ip_addr, self.um.port, "ANNOUNCEMENT", 0, None)
            print "sending announcement\n"
            myTurn_string = pickle.dumps(myTurn)
            for x in self.um.clientList :
                x.cSock.sendall(myTurn_string)
        while True:
            #start = time.time()
            #while (time.time() - start < 20) :
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN :
                    #self.update_screen()
                    
                    if self.your_turn == True:  # if already claim cards, you can never click the mouse
                        i = self.find_card(self.card_pos, event.pos)
                        if i != -1:
                            #print my_cards[i]
                            if self.redcross_flag[i] == True:
                                self.redcross_flag[i] = False
                            else:
                                self.redcross_flag[i] = True
                                
                            self.display_screen()
                            #print "can not find card!"
                        
                        i = self.find_claim_card(self.claim_card_pos, event.pos)
                        if i != -1:
                            
                            claim_no = 0
                            for flag in self.redcross_flag:
                                if flag == True:
                                    claim_no = claim_no+1
                            
                            if 0 == claim_no:
                                print 'please select your cards' 
                            else:
                                self.new_cardpics = self.discard_cards_on_table(self.redcross_flag, self.cardback)
                                print 'number: ' + str(claim_no) + ',  card: ' + self.claim_cards[i]
                                self.claim_id = i
                                self.claim_cards_ret = [claim_no, self.claim_cards[i]]
                                #self.your_turn = False
                                if len(self.out_cards) > 0 :
                                    if len(self.claim_cards_ret) > 0 :
                                        print "generating claim message\n"
                                        cardsToSend = [self.claim_cards_ret, self.out_cards]
                                        claim_msg = PeerDiscovery.Message.Msg(self.um.ip_addr, self.um.port, "CLAIM", 0, cardsToSend)
                                        claim_msg_string = pickle.dumps(claim_msg)
                                        for x in self.um.clientList :
                                            x.cSock.sendall(claim_msg_string)
                               
                                self.display_screen()  
                                          
                                start = time.time()
                                while(time.time() - start < 10) :
                                    if len(self.um.bluffMsg) > 0 :
                                        break
                                    
                                if len(self.um.bluffMsg) > 0 : 
                                    id = 0  
                                    src = self.um.bluffMsg[0].src
                                    port = self.um.bluffMsg[0].src_port
                                    for c in self.um.clientList :
                                        if c.ip == src :
                                            if c.portnum == port :
                                                un = c.username
                                    for r in self.um.respList :
                                        if r.ip_addr == src :
                                            if r.port == port :
                                                id = r.id
                                    print un, " has sent bluff request\n"
                                    print "id of node: ", id, "\n"
                                    bluffReq = PeerDiscovery.Message.Msg(self.um.ip_addr, self.um.port, "ANNOUNCE_BLUFF", 0, int(id))
                                    print "sending bluff announcement\n"
                                    bluffReq_string = pickle.dumps(bluffReq)
                                    for x in self.um.clientList :
                                        x.cSock.sendall(bluffReq_string)
                                
                                else :
                                    print "no bluff request\n"
                                        
                                            
                            self.display_screen()
                        
                                
                    
                    if self.call_bluff == True:
                        if True == self.find_call_bluff(event.pos): #return true if user clicks call bluff
                            print "Called bluff!!!"
                            print "generating bluff message\n"
                            #cardsToSend = [self.claim_cards_ret, self.out_cards]
                            bluff_msg = PeerDiscovery.Message.Msg(self.um.ip_addr, self.um.port, "BLUFF", 0, "Bluff")
                            bluff_msg_string = pickle.dumps(bluff_msg)
                            for x in self.um.clientList :
                                if x.ip == self.um.sender_ip :
                                    if x.portnum == self.um.sender_port :
                                        x.cSock.sendall(bluff_msg_string)
                                        
                            self.call_bluff = False
                            self.display_screen()
                            
                
            
            #if self.your_turn == True:
                #if len(self.out_cards) > 0 :
                   # if len(self.claim_cards_ret) > 0 :
                        #print "generating claim message\n"
                        #cardsToSend = [self.claim_cards_ret, self.out_cards]
                        #claim_msg = PeerDiscovery.Message.Msg(self.um.ip_addr, self.um.port, "CLAIM", 0, cardsToSend)
                        #claim_msg_string = pickle.dumps(claim_msg)
                        #for x in self.um.clientList :
                            #x.cSock.sendall(claim_msg_string)
                        
                        #self.update_screen()
                        #self.display_screen() #TODO: needed?
                        
                
            
            
    def display_screen(self):
        """show table cloth & card area"""
        self.screen.blit(self.background, (0,0))
        self.screen.blit(self.cardarea, self.cardarea_init_pos)
        
        '''
        i = 0
        self.my_cardpics = []
        self.card_pos = dict()
        #self.redcross_flag = []  #user put this card or not
        for card in self.my_cards:
            cardpic = pygame.image.load(card)
            cardpic = pygame.transform.scale(cardpic, self.card_size)
            self.my_cardpics.append(cardpic)
            # store card position
            x_pos = self.my_card_init_pos[0] + (i % 13)*(self.card_size[0] + 10)
            y_pos = self.my_card_init_pos[1] - (i / 13)*(self.card_size[1] + 5)
            self.card_pos[i] = (x_pos, y_pos)
            self.redcross_flag.append(False)
            i = i+1
            
        self.new_cardpics = []
        for card in self.new_cards:
            cardpic = pygame.image.load(card)
            cardpic = pygame.transform.scale(cardpic, self.card_size)
            self.new_cardpics.append(cardpic)
        '''
        
        """show my cards"""
        i = 0
        
        for cardpic in self.my_cardpics:
            x_pos = self.card_pos[i][0]
            y_pos = self.card_pos[i][1]
            if self.your_turn == False:   # already claim cards
                if self.redcross_flag[i] == False:
                   self.screen.blit(cardpic, (x_pos, y_pos)) 
            else:
                self.screen.blit(cardpic, (x_pos, y_pos))   #show cards
                if False != self.redcross_flag[i]:          #show redcross
                    self.screen.blit(self.redcrosspic, (x_pos + self.card_size[0] - self.redcross_size[0], y_pos))
            
            i = i+1
        
        """show cards on table"""
        i = 0
        for cardpic in self.new_cardpics:
            x_pos = self.cardarea_init_pos[0] + (i % 13)*(self.card_size[0] + 10)
            y_pos = self.cardarea_init_pos[1] - (i / 13)*(self.card_size[1] + 5)
            self.screen.blit(self.cardback, (x_pos, y_pos))
            i = i+1
        
        """show players list"""
        fontsize = 25
        myfont = pygame.font.SysFont("monospace", fontsize)
        label = myfont.render('Player: ' + self.me, 1, (200,200,200))
        self.screen.blit(label, self.me_player_pos)
        
        """show all players"""
        i = 0
        for player in self.player_list:
            # set different colors
            if player != self.nextp:
                label = myfont.render(player, 1, (200,200,200))
            else:
                label = myfont.render(player, 1, (255,0,0))
            x_pos = self.plyerlist_init_pos[0]
            y_pos = self.plyerlist_init_pos[1] + i * (fontsize + 5) 
            self.screen.blit(label, (x_pos, y_pos))
            i = i+1
        
        """show claim card numbers"""
        i = 0
        for claimcard in self.claim_cards:
            myfont = pygame.font.SysFont("monospace", self.claim_card_font_size)
            if self.claim_id == i:
                label = myfont.render("" + claimcard, 1, (255,0,0))
            else:
                label = myfont.render("" + claimcard, 1, (200,200,200))
            x_pos = self.claim_card_pos[i][0]
            y_pos = self.claim_card_pos[i][1]
            self.screen.blit(label, (x_pos, y_pos))
            i = i+1
        
        """If it's your turn"""
        if self.your_turn == True:
            print "****my turn check****\n"
            myfont = pygame.font.SysFont("monospace", self.claim_mark_size)
            label = myfont.render("It's your turn!", 1, (255,255,0))
            self.screen.blit(label, self.claim_mark_init_pos)
            #myTurn = PeerDiscovery.Message.Msg(self.um.ip_addr, self.um.port, "ANNOUNCEMENT", 0, None)
            #myTurn_string = pickle.dumps(myTurn)
            #for x in self.um.clientList :
                #x.cSock.sendall(myTurn_string)
                
        if self.info is not None :
            print "info not none\n"
            self.display_info(self.screen)
        
        """call bluff button"""
        if self.call_bluff == True:
            myfont = pygame.font.SysFont("monospace", self.call_bluff_size)
            label = myfont.render(self.call_bluff_str, 1, (255,255,0))
            self.screen.blit(label, self.call_bluff_init_pos)
        
        """some one call bluff"""
        if self.call_bluff_user != None:
            myfont = pygame.font.SysFont("monospace", self.call_bluff_user_size)
            label = myfont.render(self.call_bluff_user + " call bluff!", 1, (200,200,200))
            self.screen.blit(label, self.call_bluff_user_init_pos)
            
        
        """display!"""    
        pygame.display.update()
              
    def update_screen(self):
        print "****update screen****\n"
        pygame.init()
        self.screen = pygame.display.set_mode(self.table_size, 0, 32)
        
        """show table cloth"""
        background = pygame.image.load(self.table)
        self.background = pygame.transform.scale(background, self.table_size)
        
        """card area"""
        cardarea = pygame.image.load(self.card_area)
        self.cardarea = pygame.transform.scale(cardarea, self.cardarea_size)
        
        """card back"""
        cardback = pygame.image.load(self.card_back)
        self.cardback = pygame.transform.scale(cardback, self.card_size)
        
        """red cross"""
        redcrosspic = pygame.image.load(self.redcross)
        self.redcrosspic = pygame.transform.scale(redcrosspic, self.redcross_size)
        
        """get picture of cards"""
        
        i = 0
        self.my_cardpics = []
        self.card_pos = dict()
        #self.redcross_flag = []  #user put this card or not
        for card in self.my_cards:
            cardpic = pygame.image.load(card)
            cardpic = pygame.transform.scale(cardpic, self.card_size)
            self.my_cardpics.append(cardpic)
            # store card position
            x_pos = self.my_card_init_pos[0] + (i % 13)*(self.card_size[0] + 10)
            y_pos = self.my_card_init_pos[1] - (i / 13)*(self.card_size[1] + 5)
            self.card_pos[i] = (x_pos, y_pos)
            self.redcross_flag.append(False)
            i = i+1
            
        self.new_cardpics = []
        for card in self.new_cards:
            cardpic = pygame.image.load(card)
            cardpic = pygame.transform.scale(cardpic, self.card_size)
            self.new_cardpics.append(cardpic)
        
    
        """get myself & next player"""
        self.me = ''.join(self.player_list[0])
        self.nextp = ''.join(self.player_list[1])
        self.player_list.sort()
        text = ""
        
        #"""a selection menu for claim cards"""
        #self.claim_cards()
        
        """area for claim cards"""
        self.claim_cards = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
        self.claim_card_pos = dict()
        i = 0
        for claimcard in self.claim_cards:
            x_pos = self.claim_cards_init_pos[0]
            y_pos = self.claim_cards_init_pos[1] + i * (self.claim_card_font_size + 5)
            self.claim_card_pos[i] = (x_pos, y_pos)
            i = i+1
        
        """which card you claim"""
        self.claim_id = -1
        #switch = False
        print "****update screen done!****\n"
    
    def find_card(self, card_pos, mouse_pos):
        i = 0
        for c in card_pos:
            if (mouse_pos[0] >= card_pos[i][0] and mouse_pos[0] <= card_pos[i][0] + self.card_size[0] 
                and mouse_pos[1] >= card_pos[i][1] and mouse_pos[1] <= card_pos[i][1] + self.card_size[1]):
                return i
            i = i + 1
        
        return -1
    
    def find_claim_card(self, claim_card_pos, mouse_pos):
        for i in claim_card_pos:
            if (mouse_pos[0] >= claim_card_pos[i][0] and mouse_pos[0] <= claim_card_pos[i][0] + self.claim_card_size[0] 
                and mouse_pos[1] >= claim_card_pos[i][1] and mouse_pos[1] <= claim_card_pos[i][1] + self.claim_card_size[1]):
                return i
        
        return -1
    
    def find_call_bluff(self, mouse_pos):
        if (mouse_pos[0] >= self.call_bluff_init_pos[0] and mouse_pos[0] <= self.call_bluff_init_pos[0] + self.call_bluff_size * len(self.call_bluff_str) 
            and mouse_pos[1] >= self.call_bluff_init_pos[1] and mouse_pos[1] <= self.call_bluff_init_pos[1] + self.call_bluff_size):
            return True
        
        return False
         
    def claim_cards(self):
        app = wx.PySimpleApp()
        frame = ClaimBox(parent=None, id=-1)
        frame.Show()
        app.MainLoop()
    
    def discard_cards_on_table(self, card_flag, cardbackpic):
        ret_new_cards = []
        ret_remain_cards = []
        ret_out_cards = []
        print "len of my_cards: ", len(self.my_cards_in)
        print "len of redcross_cards: ", len(card_flag)
        print "discard_cards_on_table\n"
        for i in range(len(self.my_cards_in)):
            print i
            if card_flag[i] == True:
                print "true\n"
                ret_new_cards.append(cardbackpic)
                ret_out_cards.append(self.my_cards_in[i])
            else:
                print "false\n"
                ret_remain_cards.append(self.my_cards_in[i])
        
        self.remain_cards = ret_remain_cards
        self.out_cards = ret_out_cards

        print self.out_cards
        print self.remain_cards
        
        return ret_new_cards
    
    def get_remain_cards(self):
        return self.remain_cards

    def get_out_cards(self):  # block until user out cards
        while True:
            if (0 != len(self.out_cards)):
                break
        
        return self.out_cards
    
    def get_claim_cards(self):
        return self.claim_cards_ret
    
    def display_info(self, screen):
        """show plays list"""
        if self.info != None:
            fontsize = 30
            myfont = pygame.font.SysFont("monospace", fontsize)
            #print self.info
            label = myfont.render(self.info, 1, (200,200,200))
            screen.blit(label, self.info_init_pos)
        
    def close_UI(self):
        pygame.quit()
        sys.exit()
    
"""for test"""            
if __name__ == '__main__':
    cards = ['6c','7d','8h','9s']
    new_cards = ['7d','8h','9s']    
    ui = GameUI(cards, new_cards, ['qi', 'chiao', 'apoorva', 'kavya','mark'], True, False, "chiao")