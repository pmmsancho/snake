#%% Description of File

"""
This file uses the qtable approach for reinforcement learning and applies 
epsilon decay for that purposes
"""

#%% Housekeeping

# =============================================================================
# Packages
# =============================================================================
import random
import pygame
import numpy as np
import math
import pickle
import os
    
# =============================================================================
# Overall parameters
# =============================================================================
rows = 20
width = int((rows/10) * 500)
DANGER_STATES = 1
ANGLE_STATES = 360
STEP_SIZE_angle = 45
STEP_SIZE_distance = 5
EPSILON_START = 0
MAX_DISTANCE = int(round(np.sqrt(np.multiply([rows-2, rows-2],[rows-2, rows-2]).sum())))
INITIAL_VALUES = 0
show_every = 300 
rl_type = "4. master - "
clock = pygame.time.Clock()  

# =============================================================================
# Paths
# =============================================================================
qtable_path = "/Users/paulmora/Dropbox/0. Projects/2. Snake Basics/1. Output/1. RL/0. Q Tables/"
modelp_path = "/Users/paulmora/Dropbox/0. Projects/2. Snake Basics/1. Output/1. RL/1. Model Performance/"
image_path = "/Users/paulmora/Dropbox/0. Projects/2. Snake Basics/1. Output/1. RL/2. Images/"
png_path = "/Users/paulmora/Dropbox/0. Projects/2. Snake Basics/2. Images/"
music_path = "/Users/paulmora/Dropbox/0. Projects/2. Snake Basics/3. Sounds/"

#%% Creating cubes 

gameDisplay = pygame.display.set_mode((width, width))
head_img = pygame.image.load(png_path + "snakehead2.png")
berry_img = pygame.image.load(png_path + "strawberry2.png")
rabbit_img = pygame.image.load(png_path + "rabbit.png")
machine_img = pygame.image.load(png_path + "machine.png")
bad_rabbit = pygame.image.load(png_path + "rabbit2.png")
ending = pygame.image.load(png_path + "ending.png")
winning = pygame.image.load(png_path + "winning.png")
start_screen = pygame.image.load(png_path + "start_screen.png")

#%%
def snake1_direction(direction):
    if direction == "right":
        head = pygame.transform.rotate(machine_img, 270)
    if direction == "left":
        head = pygame.transform.rotate(machine_img, 90)
    if direction == "up":
        head = machine_img
    if direction == "down":
        head = pygame.transform.rotate(machine_img, 180)
    return head

def snake2_direction(direction):
    if direction == "right":
        head = pygame.transform.rotate(head_img, 270)
    if direction == "left":
        head = pygame.transform.rotate(head_img, 90)
    if direction == "up":
        head = head_img
    if direction == "down":
        head = pygame.transform.rotate(head_img, 180)
    return head

#%%
class cube1(object):
    rows = rows
    w = width
    def __init__(self, start, dirnx=1, dirny=0, color=(127,110,120)):
        self.pos = start
        self.dirnx = 1 # that makes the snake running right from the beginning 
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)
    
    def draw(self, surface, head=False):
        """
        DESCRIPTION:
        This function draws two black dots on the first cube, representing the 
        eyes of the snake
        """
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]
        
        # Creating blocks and also indicating a white line between blocks to indicate when a block starts and ends
        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2, dis-2))

#%%
class cube2(object):
    rows = rows
    w = width
    def __init__(self, start, dirnx=1, dirny=0, color=(0,140,0)):
        self.pos = start
        self.dirnx = -1 # that makes the snake running right from the beginning 
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)
    
    def draw(self, surface, head=False):
        """
        DESCRIPTION:
        This function draws two black dots on the first cube, representing the 
        eyes of the snake
        """
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]
        
        # Creating blocks and also indicating a white line between blocks to indicate when a block starts and ends
        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2, dis-2))

        
#%%  
        
direction1 = "right"

class snake1(object):
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color 
        self.head = cube1(pos)
        self.body.append(self.head)
        self.dirnx = 0 
        self.dirny = 1        
    
    def info(self):
        """
        DESCRIPTION:
        This function describes returns a list which tells whether there is an
        immediate danger around the head of the snake's head. If there is danger
        then this value equals to 1, if there is non then the value is a zero.
        Furthermore, the value of the position immediately behind the snake's head
        is given. This is necessary given the nature of the game, which would 
        allow otherwise to turn 180 degrees when the snake only consists out of
        two blocks
        
        RETURN:    
        state_info - 1x4 List - Equals 1 if there is danger and 0 if there is not
        behind_pos - 1x2 List - Shows the coordinate of the block behind the snake's head
        """                                                               
        global state_info1, behind_pos
        
# =============================================================================
# Creating the coordinates of every field next to the snake's head and then
# checking whether there is a part of the snake's body or the wall next to it
# =============================================================================
        # Show the field coordinates left to the head
        right_head = int(self.head.pos[0]+1), int(self.head.pos[1])                
        # Show the field coordinates right to the head
        left_head = int(self.head.pos[0]-1), int(self.head.pos[1])                   
        # Show the field coordinates above to the head
        below_head = int(self.head.pos[0]), int(self.head.pos[1]+1)                    
        # Show the field coordinates below to the head
        above_head = int(self.head.pos[0]), int(self.head.pos[1]-1)
        # Putting information together
        env = [right_head, left_head, above_head, below_head]
        # Creation information of the surroundings of the snake
        state_info1 = [1 if ( [position] in border_elements or position in list(map(lambda z:z.pos,snake1.body[1:])) or position in list(map(lambda z:z.pos,snake2.body[:])) ) else 0 for position in env] 

# =============================================================================
# Only using the information of the position of the second block, if the 
# snake is actually longer than 1  
# =============================================================================
        if snake1.body[0].pos != snake1.body[-1].pos: 
            behind_pos = snake1.body[1].pos
        else:
            behind_pos = None
        
# =============================================================================
# Calculating the angle of the snake's head to the apple as well as the distance
# =============================================================================
        # Calculation the head's position of the snake
        head = tuple([self.head.pos[0], self.head.pos[1]]) 
        # Subtracting the position of the snack location
        difference = np.subtract(snack_loc1, head)
        # Calculating the relative angle of the snack to the snake
        head_snack = angle(difference) 
        # Calculating the vectorial distance between two points 
        dis_snack = distance_snack(difference)
        # Appending the angle to the danger information
        state_info1.append(head_snack)
        # Appending the angle to the danger information
        state_info1.append(dis_snack) 

#%%
# =============================================================================
# Automatic Movement        
# =============================================================================
    def move(self, action):
        global direction1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        """            
        DESCRIPTION:
        This function enables the snake to move. Every direction is represented
        by a number between 0 and 3.
            
        INPUT:           
        action - 1x1 Integer - States which direction is has to go        
        """    
# =============================================================================
# Creating movement actions for every potential step in a direction
# =============================================================================
        # Left move                                        
        if action == 0:
            self.dirnx = -1
            self.dirny = 0
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            direction1 = "left"

        # Right move
        elif action == 1:
            self.dirnx = 1
            self.dirny = 0
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            direction1 = "right"
            
        # Down move
        elif action == 2:
            self.dirnx = 0
            self.dirny = 1
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            direction1 = "down"
            
        # Up move
        elif action == 3:
            self.dirnx = 0
            self.dirny = -1
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            direction1 = "up"

# =============================================================================
# Allowing for the possibility of turning 
# =============================================================================
        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
            
                if i == len(self.body)-1:
                    self.turns.pop(p)
                    
            else:
                c.move(c.dirnx,c.dirny)

           
    def reset(self,pos):
        global direction
        direction = "right"
        """
        DESCRIPTION:     
        This function resets the snake after it died. 
        
        INPUT:           
        pos - 1x2 List - Coordinates where the snake restarts
        """
        self.head = cube1(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addcube(self):
        """
        DESCRIPTION:        
        This function adds a cube to the body of the snake. It is important to 
        make that case dependend on the movement direction of the snake
        """
        
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny
        
        if dx == 1 and dy == 0:
            self.body.append(cube1((tail.pos[0]-1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube1((tail.pos[0]+1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube1((tail.pos[0], tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube1((tail.pos[0], tail.pos[1]+1)))
            
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy
        
    def draw(self, surface):
        head = snake1_direction(direction1)
        for i, c in enumerate(self.body):
            # If the program start this part tells us where the head of the snake is 
            if i == 0:
                gameDisplay.blit(head, tuple(50*x for x in snake1.body[0].pos))
            else:
                c.draw(surface)

#%%   

direction2 = "left"

class snake2(object):
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color 
        self.head = cube2(pos)
        self.body.append(self.head)
        self.dirnx = -1
        self.dirny = 0      
    
    def info(self):
        """
        DESCRIPTION:
        This function describes returns a list which tells whether there is an
        immediate danger around the head of the snake's head. If there is danger
        then this value equals to 1, if there is non then the value is a zero.
        Furthermore, the value of the position immediately behind the snake's head
        is given. This is necessary given the nature of the game, which would 
        allow otherwise to turn 180 degrees when the snake only consists out of
        two blocks
        
        RETURN:    
        state_info - 1x4 List - Equals 1 if there is danger and 0 if there is not
        behind_pos - 1x2 List - Shows the coordinate of the block behind the snake's head
        """                                                               
        global state_info2, behind_pos
        
# =============================================================================
# Creating the coordinates of every field next to the snake's head and then
# checking whether there is a part of the snake's body or the wall next to it
# =============================================================================
        # Show the field coordinates left to the head
        right_head = int(self.head.pos[0]+1), int(self.head.pos[1])                
        # Show the field coordinates right to the head
        left_head = int(self.head.pos[0]-1), int(self.head.pos[1])                   
        # Show the field coordinates above to the head
        below_head = int(self.head.pos[0]), int(self.head.pos[1]+1)                    
        # Show the field coordinates below to the head
        above_head = int(self.head.pos[0]), int(self.head.pos[1]-1)
        # Putting information together
        env = [right_head, left_head, above_head, below_head]
        # Creation information of the surroundings of the snake
        state_info2 = [1 if ( [position] in border_elements or position in list(map(lambda z:z.pos,snake2.body[1:])) or position in list(map(lambda z:z.pos,snake1.body[:])) ) else 0 for position in env] 

# =============================================================================
# Only using the information of the position of the second block, if the 
# snake is actually longer than 1  
# =============================================================================
        if snake2.body[0].pos != snake2.body[-1].pos: 
            behind_pos = snake2.body[1].pos
        else:
            behind_pos = None
        
# =============================================================================
# Calculating the angle of the snake's head to the apple as well as the distance
# =============================================================================
        # Calculation the head's position of the snake
        head = tuple([self.head.pos[0], self.head.pos[1]]) 
        # Subtracting the position of the snack location
        difference = np.subtract(snack_loc1, head)
        # Calculating the relative angle of the snack to the snake
        head_snack = angle(difference) 
        # Calculating the vectorial distance between two points 
        dis_snack = distance_snack(difference)
        # Appending the angle to the danger information
        state_info2.append(head_snack)
        # Appending the angle to the danger information
        state_info2.append(dis_snack) 

#%%
# =============================================================================
# Automatic Movement        
# =============================================================================
    def move(self):
        global direction2
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        """            
        DESCRIPTION:
        This function enables the snake to move. Every direction is represented
        by a number between 0 and 3.
            
        INPUT:           
        action - 1x1 Integer - States which direction is has to go        
        """    
# =============================================================================
# Creating movement actions for every potential step in a direction
# =============================================================================
        keys = pygame.key.get_pressed()

        for key in keys:
            if keys[pygame.K_LEFT]:
                self.dirnx = -1
                self.dirny = 0
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                direction2 = "left"

            if keys[pygame.K_RIGHT]:
                self.dirnx = 1
                self.dirny = 0
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                direction2 = "right"
                
            if keys[pygame.K_DOWN]:
                self.dirnx = 0
                self.dirny = 1
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                direction2 = "down"

            if keys[pygame.K_UP]:
                self.dirnx = 0
                self.dirny = -1
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                direction2 = "up"

# =============================================================================
# Allowing for the possibility of turning 
# =============================================================================
        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
            
                if i == len(self.body)-1:
                    self.turns.pop(p)                    
            else:
                c.move(c.dirnx,c.dirny)

           
    def reset(self,pos):
        global direction2
        direction2 = "left"
        """
        DESCRIPTION:     
        This function resets the snake after it died. 
        
        INPUT:           
        pos - 1x2 List - Coordinates where the snake restarts
        """
        self.head = cube2(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = -1
        self.dirny = 0

    def addcube(self):
        """
        DESCRIPTION:        
        This function adds a cube to the body of the snake. It is important to 
        make that case dependend on the movement direction of the snake
        """
        
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny
        
        if dx == 1 and dy == 0:
            self.body.append(cube2((tail.pos[0]-1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube2((tail.pos[0]+1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube2((tail.pos[0], tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube2((tail.pos[0], tail.pos[1]+1)))
            
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy
        
    def draw(self, surface):
        head = snake2_direction(direction2)
        for i, c in enumerate(self.body):
            # If the program start this part tells us where the head of the snake is 
            if i == 0:
                gameDisplay.blit(head, tuple(50*x for x in snake2.body[0].pos))
            else:
                c.draw(surface)

       
def drawGrid(w, rows, surface):
    """
    DESCRIPTION:
    This function creates the gridlines of the board. Further, it assigns a 
    certain color to these lines. The function is dependend on the width and 
    row number of the desired size of the game
    
    INPUT:
    w - 1x1 Integer - Number indicating the pixel width of the game
    rows - 1x1 Integer - Number indicating how many rows the game should have
    surface - Object - The object on which the function is applied on
    """
    
    # Creating the number of pixels between two gridlines 
    sizeBtwn = w // rows
    color_grid = (192,192,192)
    x = 0
    y = 0
    # The number of rows is reduced by three since the outer layer is a wall
    for l in range(rows-3):
        x = x + (sizeBtwn)
        y = y + (sizeBtwn)
        
        pygame.draw.line(surface, color_grid, (x+sizeBtwn,sizeBtwn), (x+sizeBtwn,w-sizeBtwn))
        pygame.draw.line(surface, color_grid, (sizeBtwn,y+sizeBtwn), (w-sizeBtwn,y+sizeBtwn))

def redrawWindow(surface, points1, points2, deaths1, deaths2, counter):
    """
    DESCRIPTION:
    This function re-creates the window after the snake dies
    """  
    global rows, width, snake1, snack1, snake2, snack2
        
    # Colors
    inside = (255,255,255)
    outside = (0,0,0)
    
    # Draw the gaming field in black
    surface.fill(inside)

    # Drawing the borders of the playing field 
    sizeBtwn = width // rows
    pygame.draw.rect(surface, outside, [0, 0, width, sizeBtwn])
    pygame.draw.rect(surface, outside, [0, width-sizeBtwn, width, sizeBtwn])
    pygame.draw.rect(surface, outside, [0, 0, sizeBtwn, width])
    pygame.draw.rect(surface, outside, [width-sizeBtwn, 0, sizeBtwn, width])
    
    snake1.draw(surface)
    snake2.draw(surface)
    snack1 = gameDisplay.blit(bad_rabbit, tuple(50*x for x in snack_loc1))
    snack2 = gameDisplay.blit(rabbit_img, tuple(50*x for x in snack_loc2))
    drawGrid(width, rows, surface)
    score(surface, points1, points2, deaths1, deaths2, counter)
    pygame.display.update()

def score(surface, points1, points2, deaths1, deaths2, counter): 
    global average, average1, average2

    average1 = round(points1 / deaths1, 2)
    average2 = round(points2 / deaths2, 2)
    
    machine_score = middlefont.render("Machines' Avg: " + str(average1), True, (255,255,255))
    human_score = middlefont.render(str(average2) + ": Humans' Avg " , True, (255,255,255))
    time_left = middlefont.render("Time left: " + str(round(counter,2))  , True, (255,255,255))
 
    
    surface.blit(machine_score , [0, 0])
    surface.blit(human_score, [700, 0])
    surface.blit(time_left, [350, 950])

     
def randomSnack1(rows, item1, item2):
    """
    DESCIRPTION:
    This function creates a snack somewhere in the field. It is ensured that
    the snack is not spawned within the wall or the snake
    
    INPUT:
    rows - 1x1 Integer - Indicates how large the gamefield is  
    item - Snake Object - Snake object for determining its positions
    """
    
    position1 = item1.body
    position2 = item2.body
    while True:
        snack_x = random.randrange(1,rows-1) 
        snack_y = random.randrange(1,rows-1) 
        if len(list(filter(lambda z: z.pos == (snack_x, snack_y), position1))) > 0:
            continue 
        elif len(list(filter(lambda z: z.pos == (snack_x, snack_y), position2))) > 0:
            continue 
            
        else : 
            break
    return (snack_x, snack_y)

def randomSnack2(rows, item1, item2):
    """
    DESCIRPTION:
    This function creates a snack somewhere in the field. It is ensured that
    the snack is not spawned within the wall or the snake
    
    INPUT:
    rows - 1x1 Integer - Indicates how large the gamefield is  
    item - Snake Object - Snake object for determining its positions
    """
    
    position1 = item1.body
    position2 = item2.body
    while True:
        snack_x = random.randrange(1,rows-1) 
        snack_y = random.randrange(1,rows-1) 
        if len(list(filter(lambda z: z.pos == (snack_x, snack_y), position1))) > 0:
            continue 
        elif len(list(filter(lambda z: z.pos == (snack_x, snack_y), position2))) > 0:
            continue 
            
        else : 
            break
    return (snack_x, snack_y)

# Defining the font 
pygame.font.init()
middlefont = pygame.font.SysFont("comicsansms", 50)
smallfont = pygame.font.SysFont("comicsansms", 25)

# Putting messages to screen
def message_to_screen(msg, color, location, font):
    screen_text = font.render(msg, True, color)
    gameDisplay.blit(screen_text, location)
    pygame.display.update()
  
# Angle rounded to the nearest five so there the number of angles does not explode
def myround_angle(x, base=STEP_SIZE_angle):
    """
    DESCRIPTION:
    Function that rounds a float variable to its nearest base
        
    INPUT:
    x - 1x1 Scalar - Which will be rounded to the next Step Size
    base - 1x1 Scalar - What is the step size
    """
    return base * round(x/base)

def myround_distance(x, base=STEP_SIZE_distance):
    """
    DESCRIPTION:
    Function that rounds a float variable to its nearest base
        
    INPUT:
    x - 1x1 Scalar - Which will be rounded to the next Step Size
    base - 1x1 Scalar - What is the step size
    """
    return base * round(x/base)

def angle(location):
    """
    DESCRIPTION:
    This function determines the angle between the snake's head and the snack
        
    INPUT:
    location - 1x2 List - Coordinates of where the snack is relatively to the snake
    """
    x = location[0]
    y = location[1]
    
    radian = math.atan2(x, y)

    if radian < 0:
        angle = 360 + math.degrees(radian)
    else:
        angle = math.degrees(radian)
        
    return myround_angle(angle)

def distance_snack(location):
    """
    DESCRIPTION:
    Calcualting the distance of the snack to the snake's head
    
    INPUT:
    location - 1x2 List - Coordinates of the snack, using the snake's head as the origin
    """
    distance = np.sqrt(np.multiply(location,location).sum())
    normed_distance = myround_distance(distance)
    
    return int(normed_distance)

pygame.init()
def kill_sound():
    # Getting random killing sound
    number = np.random.randint(0,10)
    killing_sound = pygame.mixer.Sound(music_path  + str(number) + ".wav")
    # Play sound 
    pygame.mixer.Sound.play(killing_sound)

ending_sound = pygame.mixer.Sound(music_path + "Ending.wav")

def game_intro():
    
    intro = True   
    while intro:
        
        # Pressing c or q logic
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                
        gameDisplay.blit(start_screen, [0, 0])
        message_to_screen("Start - Press C",
                  (255, 255, 255),
                  [width/2 - 400, width/2 - 200],
                  middlefont)
        message_to_screen("Quit - Press Q",
                  (255, 255, 255),
                  [width/2 - 400, width/2 - 150],
                  middlefont)
        pygame.display.update()
        clock.tick(15)
        
def game_outro(points1, points2):
    global gameOver, snake1, snake2
    
    outro = True   
    while outro:
        
        # Pressing c or q logic         
        for event1 in pygame.event.get():
            if event1.type == pygame.QUIT:
                pygame.quit()
                quit()
                
            if event1.type == pygame.KEYDOWN:
                if event1.key == pygame.K_c:
                    outro = False
                    gameOver = False
                    counter = 60    
                    points1 = 0
                    points2 = 0
                    deaths1 = 1
                    deaths2 = 1
                    snake1.reset(((rows/2), (rows/2)))
                    snake2.reset(((rows/2), (rows/2)))
                if event1.key == pygame.K_q:
                    gameExit = True
                    pygame.display.quit()
                    pygame.quit()
        
        if points1 > points2:
            gameDisplay.blit(ending, [0, 0])    
            pygame.mixer.Sound.play(ending_sound)
            message_to_screen("Press C to play again or Q to leave", 
                              (255,255,255), 
                              ((width/2), (width/2+ 50)), 
                              smallfont)
            message_to_screen("The machine was " + str(round((average1/ average2),2)) + " times better than you", 
                              (255,0,0), 
                              ((width/2 - 350), (width/2+ 100)), 
                              middlefont)
            pygame.display.update()
        else :
            gameDisplay.blit(winning, [0, 0])
            message_to_screen("You are truly the one", 
                              (255,255,255), 
                  ((width/2), (width/2)), 
                  middlefont)
            message_to_screen("Press C to play again or Q to leave", 
                              (255,0,0), 
                              ((width/2), (width/2+ 50)), 
                              smallfont)
            pygame.display.update()
    
    return gameOver, counter, snake1, snake2, points1, points2, deaths1, deaths2

# Initialising the values of the border
border_elements = []
for l in range(rows):
    border_elements.append([(0,l)])
    border_elements.append([(rows-1,l)])
    border_elements.append([(l,0)])
    border_elements.append([(l,rows-1)])

q_table_path_file = "/USERS/paulmora/Dropbox/0. Projects/2. Snake Basics/1. Output/1. RL/0. Q Tables/4. master - qtable.p"

if os.path.isfile(q_table_path_file):
    q_table = pickle.load( open( q_table_path_file, "rb" ) )

           
#%% 
        
def main():
    """
    Function to initalise the game. 
    """    
# =============================================================================
# Getting values needed for the later function    
# =============================================================================
    # These information is assigned later 
    global width, rows, snake1, snake2, snack1, snack2, points1, points2, snack_loc1, snack_loc2, epsilon, episode_rewards, len_moves, len_body 
    # Board parameter
    width = width
    # Board parameter
    rows = rows 
    # Creating the snake
    snake1 = snake1((255,0,0), ((rows/2), (rows/2)+2)) 
    snake2 = snake2((255,0,0), ((rows/2), (rows/2)))
    # Visualising the game
    win = pygame.display.set_mode((width, width)) 
    # Determining the location of the snack
    snack_loc1 = randomSnack1(rows,snake1, snake2)
    snack_loc2 = randomSnack2(rows,snake1, snake2)
    # Creation of the snack as well as assigning information
    snack1 = gameDisplay.blit(bad_rabbit, tuple(50*x for x in snack_loc1))
    snack2 = gameDisplay.blit(rabbit_img, tuple(50*x for x in snack_loc2))

# =============================================================================
# Initialising lists and hard coded values
# =============================================================================
    points1 = 0
    points2 = 0
    deaths1 = 1
    deaths2 = 1
    counter = 60
    gameOver = False
    gameExit = False        
    
# =============================================================================
# Running all N rounds
# =============================================================================

    while gameExit == False:
                        
        while gameOver == True:
            gameOver, counter, snake1, snake2, points1, points2, deaths1, deaths2 = game_outro(points1, points2) 

        while gameOver == False:
            while 0 < counter:
                # Time increase
                counter -= 1/10
                # Speed of the game 
                clock.tick(10)
                # Creating state information 
                snake1.info() 
                snake2.info()
                # Tupling the information of the state   
                obs1 = tuple(state_info1) 
                # Gradually using more the known stuff, exploiting
                # We are not interested in the actual value, but only which position is maximising, hence argmax
                action1 = np.argmax(q_table[obs1]) 
                # Moving in the direction predicted by the q table or by the random move        
                snake1.move(action1)     
                snake2.move()            
                # Creating the event when snake is eating a snack
                if snake1.body[0].pos == snack_loc1:
                    # Increasing score
                    points1 += 1
                    # When the snake is eating the cube then we add a cube
                    snake1.addcube()
                    # Getting the new location of the snack
                    snack_loc1 = randomSnack1(rows,snake1, snake2)
                    # After the snack is gone, another cube has to be initalisied
                    snack1 = cube1(snack_loc1, color=(0,255,0))
                    # Bunny sound
                    kill_sound()
                    
                # Creating the event when snake is eating a snack
                if snake2.body[0].pos == snack_loc2:
                    # Increasing score
                    points2 += 1
                    # When the snake is eating the cube then we add a cube
                    snake2.addcube()
                    # Getting the new location of the snack
                    snack_loc2 = randomSnack2(rows,snake1, snake2)
                    # After the snack is gone, another cube has to be initalisied
                    snack2 = cube2(snack_loc2, color=(0,255,0))
                    # Bunny sound
                    kill_sound()
                    
                # Events that happen when the snake hits the enemy
                if ([snake1.body[0].pos] in border_elements) or (snake1.body[0].pos in list(map(lambda z:z.pos,snake1.body[1:]))) or (snake1.body[0].pos in list(map(lambda z:z.pos,snake2.body[:]))) or (snake1.body[0].pos == behind_pos):   
                    # Increasing number of deaths
                    deaths1 += 1
                    # Reseting the game
                    snake1.reset(( (rows/2)-1, (rows/2) ))
        
                # Events that happen when the snake hits the enemy
                if ([snake2.body[0].pos] in border_elements) or (snake2.body[0].pos in list(map(lambda z:z.pos,snake2.body[1:]))) or (snake2.body[0].pos in list(map(lambda z:z.pos,snake1.body[:]))) or (snake2.body[0].pos == behind_pos): 
                    # Increasing number of deaths
                    deaths2 += 1
                    # Reseting the game
                    snake2.reset(((rows/2), (rows/2)))
        
                # Needed to restart the visual game
                redrawWindow(win, points1, points2, deaths1, deaths2, counter)
            gameOver = True
                
game_intro()
pygame.mixer.music.stop()
main()


#%% Quitting game 

pygame.display.quit()
pygame.quit()