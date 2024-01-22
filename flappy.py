#Name: flappy.py
#Author: Coding With Russ
#Date: 1/21/24
#Purpose: Code flappy bird into pygame

#Tutorial 1-3

#Import
import pygame
#Import everything from pygame
from pygame.locals import *

#Initialize pygame
pygame.init()

#Set clock and framerate
clock = pygame.time.Clock()
fps = 60


#Set width and height of the pop up screen
screen_width = 450
screen_height = 450

#This is making the actual screen with the screen width and height as parameters for the function
screen = pygame.display.set_mode((screen_width, screen_height))

#Add a caption to the window
pygame.display.set_caption("Flappy Bird")


#Define game variables
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
#---------------------IMAGES-------------------------------------

#Background sky
bg = pygame.image.load('sky_bg.jpg')

#Ground
ground = pygame.image.load('floor.png')




#----------------------------------------------------------------

#-------------------BIRD CLASS-----------------------------

#Make a class with pygame with sprite functions
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        #Set up list of images to go through while game
        #Is running. Kind of like a flipbook
        self.images = []
        self.index = 0

        #Control animation speed
        self.counter = 0

        #Going through the list to set off animations
        for num in range(1,4):
            img = pygame.image.load(f'flappy_{num}.png')
            self.images.append(img)

        #Set image
        self.image = self.images[self.index]

        #Setting hit box
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]

        #Set velocity
        self.vel = 0

        #Set clicked variable
        self.clicked = False

    def update(self):

        #If the game has started
        if flying == True:
            #Gravity
            #Set velocity of gravity
            self.vel += 0.2

            #Set cap to velocity
            if self.vel > 8:
                self.vel = 8

            #If flappy hits the bottom, just stay at the bottom
            if self.rect.bottom < 300:  
                self.rect.y += int(self.vel)

        #This is essentially a toggle to stop animation if the game ends
        if game_over == False:
            #Jumping
            #If the player clicked the LMB AND the user hasn't clicked yet, jump
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -5
            #If the user is not clicking, reset the clicked variable to false
            if pygame.mouse.get_pressed()[0] == 0: 
                self.clicked = False


            #Handle the animation
            self.counter += 1
            flap_cooldown = 5

            #If the counter goes above 5, go to the next image in the list
            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1

                #If the index value is greater than the amount of
                #Images in the list, reset back to zero
                if self.index >= len(self.images):
                    self.index = 0
            #Set image
            self.image = self.images[self.index]

            #rotate the bird depending on the velocity
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)

        #If game is over, make the bird face into the ground
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)
#Keeps track of sprites
bird_group = pygame.sprite.Group()

#Create object
flappy = Bird(100, int(screen_height / 3))

#Add flappy into the sprite group
bird_group.add(flappy)


#Set up game loop
run = True
while run:

    #Set to 60 fps
    clock.tick(fps)


    #Draw background
    screen.blit(bg, (0,0))

    #Bird
    bird_group.draw(screen)
    bird_group.update()

    #Draw and scroll ground
    screen.blit(ground, (ground_scroll ,300))

    #Check if bird has hit the ground
    #If so, the game has ended
    if flappy.rect.bottom > 290:
        game_over = True
        flying = False


    if game_over == False:
        #Will make the ground go to the left
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 40:
            ground_scroll = 0
    

    #Get all events that are happening
    for event in pygame.event.get():
        #If any event type is equal to just closing out of the window, end loop
        if event.type == pygame.QUIT:
            run = False
        #Check if the player has clicked yet. If yes, then the game starts
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True

    pygame.display.update()

pygame.quit()