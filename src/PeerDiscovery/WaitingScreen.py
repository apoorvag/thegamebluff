'''
Created on Apr 15, 2013

@author: Kavya
'''

import pygame, sys, pygame.font, pygame.event, pygame.draw, string
from pygame.locals import *


class Button():
    """Class used to create a button, use setCords to set 
        position of topleft corner. Method pressed() returns
        a boolean and should be called inside the input loop."""
    def __init__(self, text, x, y, screen):
        #self.image, self.rect = load_image('button.png', -1)
        self.rect = pygame.Rect(x, y, 50, 30)
        self.text = text
        fontobj = pygame.font.SysFont('calibri', 18)
        screen.blit(fontobj.render(self.text, 1, (255,255,255)),
                ((screen.get_width() / 2) - 95, (screen.get_height() / 2) + 110))
        pygame.display.flip()
    #def setCords(self,x,y):
        #self.rect.topleft = x,y

    def pressed(self,mouse):
        if mouse[0] > self.rect.topleft[0]:
            if mouse[1] > self.rect.topleft[1]:
                if mouse[0] < self.rect.bottomright[0]:
                    if mouse[1] < self.rect.bottomright[1]:
                        return True
                    else: return False
                else: return False
            else: return False
        else: return False
        
def get_key():
  while 1:
    event = pygame.event.poll()
    if event.type == KEYDOWN:
      return event.key
    else:
      pass

def display_box(screen, message):
  "Print a message in a box in the middle of the screen"
  fontobject = pygame.font.SysFont('calibri', 32)
  
  
  pygame.draw.rect(screen, (0,0,0),
                   ((screen.get_width() / 2) - 150,
                    (screen.get_height() / 2) - 100,
                    300,100), 0)
  pygame.draw.rect(screen, (255,255,255),
                   ((screen.get_width() / 2) - 152,
                    (screen.get_height() / 2) - 102,
                    304,104), 1)
  if len(message) != 0:
    screen.blit(fontobject.render(message, 1, (255,255,255)),
                ((screen.get_width() / 2) - 150, (screen.get_height() / 2) - 70))
  pygame.display.flip()

def ask(screen, question):
  "ask(screen, question) -> answer"
  pygame.font.init()
  current_string = []
  display_box(screen, question + ": " + string.join(current_string,""))
  while 1:
    inkey = get_key()
    if inkey == K_BACKSPACE:
      current_string = current_string[0:-1]
    elif inkey == K_RETURN:
      break
    elif inkey <= 127:
      current_string.append(chr(inkey))
    display_box(screen, question + ": " + string.join(current_string,""))
  return string.join(current_string,"")

#def options(screen):
    
    
def main():
  screen = pygame.display.set_mode((600,600))
  #print ask(screen, "Name") + " was entered"
  
  name = ask(screen, "Name")    
  print name
  
  x = (screen.get_width() / 2) - 100
  y = (screen.get_height() / 2) + 100
  button = Button("Start", x, y, screen) #Button class is created
    #button.setCords(200,200) #Button is displayed at 200,200
  while True:
      
      for event in pygame.event.get():
          if event.type == MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if button.pressed(mouse):   #Button's pressed method is called
                    print ('button hit')
                    
          if event.type == QUIT: # can close only after i enter name?
              pygame.quit()
              sys.exit()
              
      pygame.display.update()
  
  
  #print pygame.font.get_fonts()
  


if __name__ == '__main__': main()




'''
pygame.init()
DISPLAYSURF = pygame.display.set_mode((1000, 900))
pygame.display.set_caption('Bluff')
WHITE = (255, 255, 255)
font = pygame.font.Font(None, 32)
text = font.render('Waiting for Responses', True, (0, 0, 255), WHITE)
while True: # main game loop
    DISPLAYSURF.blit(text, pygame.draw.rect(DISPLAYSURF, WHITE, [100,100,800,100], 0))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
'''