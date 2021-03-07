# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 17:15:19 2021

@author: qwang
"""
import random
import pygame
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

sounds=['baa','meow','oink','woof','moo','hoot','quack','buzzzz','ribbet']
animal=['sheep','cat','pig','dog','cow','owl','duck','bee','frog']

class Menu(object):
    state = -1
    def __init__(self,items,font_color=(0,0,0),select_color=(255,0,0),ttf_font=None,font_size=25):
        self.font_color = font_color
        self.select_color = select_color
        self.items = items
        self.font = pygame.font.Font(ttf_font,font_size)
        # Generate a list that will contain the rect for each item
        self.rect_list = self.get_rect_list(items)
    
    def get_rect_list(self,items):
        rect_list = []
        for index, item in enumerate(items):
            # determine the amount of space needed to render text
            size = self.font.size(item)
            # Get the width and height of the text
            width = size[0]
            height = size[1]
    
            posX = (SCREEN_WIDTH / 2) - (width /2)
            # t_h: total heigth of the text block
            t_h = len(items) * height
            posY = (SCREEN_HEIGHT /2) - (t_h /2) + (index * height)
            # Create rects
            rect = pygame.Rect(posX,posY,width,height)
            # Add rect to the list
            rect_list.append(rect)
    
        return rect_list
    
    def collide_points(self):
        index = -1
        mouse_pos = pygame.mouse.get_pos()
        for i,rect in enumerate(self.rect_list):
            if rect.collidepoint(mouse_pos):
                index = i
    
        return index
    
    def update(self):
        # assign collide_points to state
        self.state = self.collide_points()
        
    def display_frame(self,screen):
        for index, item in enumerate(self.items):
            if self.state == index:
                label = self.font.render(item,True,self.select_color)
            else:
                label = self.font.render(item,True,self.font_color)
            
            width = label.get_width()
            height = label.get_height()
            
            posX = (SCREEN_WIDTH /2) - (width /2)
            # t_h: total height of text block
            t_h = len(self.items) * height
            posY = (SCREEN_HEIGHT /2) - (t_h /2) + (index * height)
            
            screen.blit(label,(posX,posY))
# Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,128)
    
class Game(object):
    def __init__(self):
        # Create a new font obeject
        self.font = pygame.font.Font(None,65)
        # Create font for the score msg
        self.score_font = pygame.font.Font("kenvector_future.ttf",20)
        # Create a dictionary with keys: num1, result
        # These variables will be used for creating the word problem
        self.problem = {"word1":0,"result":0}
        # Create a variable that will hold the name of the operation
        self.operation = ""
        self.button_list = self.get_button_list()
        # Create boolean that will be true when clicked on the mouse button
        # This is because we have to wait some frames to be able to show
        # the rect green or red.
        self.reset_problem = False
        # Create menu
        items = ("Start","")
        self.menu = Menu(items,ttf_font="XpressiveBlack Regular.ttf",font_size=50)
        # True: show menu
        self.show_menu = True
        # create the score counter
        self.score = 0
        # Count the number of problems
        self.count = 0
        # load background image
        self.background_image = pygame.image.load("animal.jpg").convert()
        # load sounds effects
        self.sound_1 = pygame.mixer.Sound("item1.ogg")
        self.sound_2 = pygame.mixer.Sound("item2.ogg")
    
    def get_button_list(self):
        """ Return a list with four buttons """
        button_list = []
        # assign one of the buttons with the right answer
        choice = random.randint(1,4)
        # define the width and height
        width = 100
        height = 100
        # t_w: total width
        t_w = width * 2 + 50
        posX = (SCREEN_WIDTH / 2) - (t_w /2)
        posY = 150

        same=0
        while same<8:
            i=random.sample(range(0, 8), 4)
            for number in i:
                if self.problem["result"]==animal[number]:
                    same=0
                else:
                    same+=2
                
        #print('same=',same)        note: for testing purposes only
        #print('i=',i)

        if choice == 1:
            btn = Button(posX,posY,width,height,self.problem["result"])
            button_list.append(btn)
        else:
            btn = Button(posX,posY,width,height,animal[i[0]])
            button_list.append(btn)
    
        posX = (SCREEN_WIDTH / 2) - (t_w/2) + 150
        if choice == 2:
            btn = Button(posX,posY,width,height,self.problem["result"])
            button_list.append(btn)
        else:
            btn = Button(posX,posY,width,height,animal[i[1]])
            button_list.append(btn)
    
        posX = (SCREEN_WIDTH / 2) - (t_w /2)
        posY = 300
    
        
        if choice == 3:
            btn = Button(posX,posY,width,height,self.problem["result"])
            button_list.append(btn)
        else:
            btn = Button(posX,posY,width,height,animal[i[2]])
            button_list.append(btn)
    
        posX = (SCREEN_WIDTH / 2) - (t_w/2) + 150
            
        if choice == 4:
            btn = Button(posX,posY,width,height,self.problem["result"])
            button_list.append(btn)
        else:
            btn = Button(posX,posY,width,height,animal[i[3]])
            button_list.append(btn)

    
        return button_list
    
    

    
    def get_image(self,sprite_sheet,x,y,width,height):
        """ This method will cut an image and return it """
        # Create a new blank image
        image = pygame.Surface([width,height]).convert()
        # Copy the sprite from the large sheet onto the smaller
        image.blit(sprite_sheet,(0,0),(x,y,width,height))
        # Return the image
        return image
    def animal(self):
        """ set animals for sound"""
        a = random.randint(0,8)
        #print(a)  note: for testing purposes only
        self.problem["word1"] = sounds[a]
        self.problem["result"] = animal[a]
        self.operation= "Start"
        
        

    
    
    def check_result(self):
        """ Check the result """
        for button in self.button_list:
            if button.isPressed():
                if button.get_text() == self.problem["result"]:
                    # set color to green when correct
                    button.set_color(GREEN)
                    # increase score
                    self.score += 20
                    # Play sound effect
                    self.sound_1.play()
                else:
                    # set color to red when incorrect
                    button.set_color(RED)
                    # play sound effect
                    self.sound_2.play()
                # Set reset_problem True so it can go to the
                # next problem
                # we'll use reset_problem in display_frame to wait
                # a second
                self.reset_problem = True
    
    def set_problem(self):
        """ do another problem again """ 
        if self.operation == "Start":
            self.animal()
        
        self.button_list = self.get_button_list()
        
    
    def process_events(self):
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT: # If user clicked close
                return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.show_menu:
                    if self.menu.state == 0:
                        self.operation = "Start"
                        self.set_problem()
                        self.show_menu = False
                    elif self.menu.state == 1:
                        self.operation = ""
                        self.set_problem()
                        self.show_menu = False

                # We'll go to check_result to check if the user
                # answer correctly the problem
                else:
                    self.check_result()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.show_menu = True
                    # set score to 0
                    self.score = 0
                    self.count = 0
    
        return False
    
    def run_logic(self):
        # Update menu
        self.menu.update()
    
        
    def display_message(self,screen,items):
        """ display every string that is inside of a tuple(args) """
        for index, message in enumerate(items):
            label = self.font.render(message,True,GREEN)
            # Get the width and height of the label
            width = label.get_width()
            height = label.get_height()
            
            posX = (SCREEN_WIDTH /2) - (width /2)
            # t_h: total height of text block
            t_h = len(items) * height
            posY = (SCREEN_HEIGHT /2) - (t_h /2) + (index * height)-100
            
            screen.blit(label,(posX,posY))
              
    
    def display_frame(self,screen):
        # Draw the background image
        screen.blit(self.background_image,(0,0))
        # True: call pygame.time.wait()
        time_wait = False
        # --- Drawing code should go here
        if self.show_menu:
            self.menu.display_frame(screen)
        elif self.count == 5:
            # if the count gets to 5 that means that the game is over
            # and we are going to display how many answers were correct
            # and the score
            msg_1 = "You answered " + str(self.score / 20) + " correctly"
            msg_2 = "Your score was " + str(self.score)
            self.display_message(screen,(msg_1,msg_2))
            self.show_menu = True
            # reset score and count to 0
            self.score = 0
            self.count = 0
            # set time_wait True to wait 3 seconds
            time_wait = True
        else:
            # Create labels for the each number
            #label_1 = self.font.render("How do you spell the name of the animal that says",True,BLACK)
            #print(type(self.problem["word1"]))
            label_1 = self.font.render(str(self.problem["word1"]),True,BLACK)
            #label_2 = self.font.render(str(self.problem["word1"]),True,BLACK)
            # t_w: total width
            t_w = label_1.get_width()# + label_2.get_width() + 64 # 64: length of symbol
            posX = (SCREEN_WIDTH / 2) - (t_w / 2)
            screen.blit(label_1,(posX,50))
            
            #screen.blit(label_2,(posX + label_1.get_width() + 64,50))
            for btn in self.button_list:
                btn.draw(screen)
            # display the score
            score_label = self.score_font.render("Score: "+str(self.score),True,BLACK)
            screen.blit(score_label,(10,10))
            
        # --- Go ahead and update the screen with what we've drawn
        pygame.display.flip()
        # --- This is for the game to wait a few seconds to be able to show
        # --- what we have drawn before it change to another frame
        if self.reset_problem:
            # wait 1 second
            pygame.time.wait(1000)
            self.set_problem()
            # Increase count by 1
            self.count += 1
            self.reset_problem = False
        elif time_wait:
            # wait three seconds
            pygame.time.wait(3000)
    
class Button(object):
    def __init__(self,x,y,width,height,word):
        self.rect = pygame.Rect(x,y,width,height)
        self.font = pygame.font.Font(None,40)
        self.text = self.font.render(str(word),True,BLACK)
        self.word = word
        self.background_color = WHITE
    
    def draw(self,screen):
        """ This method will draw the button to the screen """
        # First fill the screen with the background color
        pygame.draw.rect(screen,self.background_color,self.rect)
        # Draw the edges of the button
        pygame.draw.rect(screen,BLUE,self.rect,3)
        # Get the width and height of the text surface
        width = self.text.get_width()
        height = self.text.get_height()
        # Calculate the posX and posY
        posX = self.rect.centerx - (width / 2)
        posY = self.rect.centery - (height / 2)
        # Draw the image into the screen
        screen.blit(self.text,(posX,posY))
    
    def isPressed(self):
        """ Return true if the mouse is on the button """
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            return True
        else:
            return False
    
    def set_color(self,color):
        """ Set the background color """
        self.background_color = color
    
    def get_text(self):
        """ Return the word of the button."""
        return self.word
    
    
def main():
    # Initialize all imported pygame modules
    pygame.init()
    # Set the width and height of the screen [width, height]
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    # Set the current window caption
    pygame.display.set_caption("Word Game")
    #Loop until the user clicks the close button.
    done = False
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    # Create game object
    game = Game()
    # -------- Main Program Loop -----------
    while not done:
        # --- Process events (keystrokes, mouse clicks, etc)
        done = game.process_events()
        # --- Game logic should go here
        game.run_logic()
        # --- Draw the current frame
        game.display_frame(screen)
        # --- Limit to 30 frames per second
        clock.tick(30)
    
    # Close the window and quit.
    # If you forget this line, the program will 'hang'
    # on exit if running from IDLE.
    pygame.quit()


if __name__ == '__main__':
    main() 
    
    
    
    
    
    
    
    
    
    
    
