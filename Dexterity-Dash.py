# Houses bigger, fixed locations, titles for stations, exit house
# tracking: time limit, use different joysticks, switch fruits
# original collecting game: collecting in certain time
# pattern game: arrows move down, check collision and joystick pos, 3 fingers, increase speed after certain score

import pygame
import sys
import os
import subprocess
import random
from joystick_library import *

joystick1 = Joystick("4B",1,0)
joystick2 = Joystick("4B",2,3)
joystick3 = Joystick("48",3,2)
joystick4 = Joystick("49",1,0)
joystick5 = Joystick("49",2,3)

# MOVE THIS DOWN INTO GAME LOOP AFTER COLLISION

def update_highscores():
    f = open("highscores.txt", "r")
    highscores = []

    for line in f:
        line = line.split()
        highscores.append(int(line[-1]))

    f.close()
    return highscores

highscores = update_highscores()


# Initialize Pygame
pygame.init()

# Set window dimensions
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 1280

# Set colors
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

# Create window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Set caption
pygame.display.set_caption("Dexterity-Dash")

# Set clock
clock = pygame.time.Clock()

# Set box dimensions
BOX_WIDTH = 50
BOX_HEIGHT = 50

box_img = pygame.image.load('player.png')
box_img = pygame.transform.scale(box_img, (BOX_WIDTH, BOX_HEIGHT))
inverted_box_img = pygame.transform.flip(box_img, True, False)

# Set box position
box_x = WINDOW_WIDTH // 2
box_y = WINDOW_HEIGHT // 2

# Set box speed
box_speed = 1

# Set direction constants
LEFT = 'left'
RIGHT = 'right'
UP = 'up'
DOWN = 'down'

# Set initial direction
direction = RIGHT

# Load station images
station1_img = pygame.image.load('house1.png')
station2_img = pygame.image.load('house2.png')
station3_img = pygame.image.load('house3.png')
exit_img = pygame.image.load('house4.png')

# Scale the station images to the desired size
station1_img = pygame.transform.scale(station1_img, (100, 100))
station2_img = pygame.transform.scale(station2_img, (100, 100))
station3_img = pygame.transform.scale(station3_img, (100, 100))
exit_img = pygame.transform.scale(exit_img, (100, 100))

# Define station rectangles to be spawned at set locations
station1_rect = station1_img.get_rect()
station1_rect.x = 300
station1_rect.y = 100

station2_rect = station2_img.get_rect()
station2_rect.x = 800
station2_rect.y = 100

station3_rect = station3_img.get_rect()
station3_rect.x = 570
station3_rect.y = 750

exit_rect = exit_img.get_rect()
exit_rect.x = WINDOW_WIDTH - exit_img.get_width()
exit_rect.y = WINDOW_HEIGHT - exit_img.get_height()

# Define station actions
station1_action = "station1.py"
station2_action = "station2.py"
station3_action = "station3.py"

# Create a font object
title_font = pygame.font.Font('font.otf',140)
header_font = pygame.font.Font('font.otf', 48)
text_font = pygame.font.Font("font.otf", 36)

# Load splash screen image
splash_screen = pygame.image.load('Background.PNG')
splash_text = title_font.render("Dexterity Dash", True, blue)


# Scale the splash screen image to fit the window size
splash_screen = pygame.transform.scale(splash_screen, (WINDOW_WIDTH, WINDOW_HEIGHT))


# Display splash screen
screen.blit(splash_screen, (0, 0))
screen.blit(splash_text, (230, 500))
pygame.display.flip()

# Wait for 2 seconds
pygame.time.wait(4000)

# Load background image
background = pygame.image.load('Best.PNG')

# Scale the background image to fit the window size
background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))

# Display background image
screen.blit(background, (0, 0))
pygame.display.flip()

#Set initial box velocities
box_vel_x = 0
box_vel_y = 0



# Render the text onto a surface

text_header = header_font.render(f"Highscores:", True, blue)
text_st1 = text_font.render(f"Mode 1: {highscores[0]}", True, blue)
text_st2 = text_font.render(f"Mode 2: {highscores[1]}", True, blue)
text_st3 = text_font.render(f"Mode 3: {highscores[2]}", True, blue)
text_station1 = text_font.render(f"Mode 1: Pattern", True, blue)
text_station2 = text_font.render(f"Mode 2: Collecting", True, blue)
text_station3 = text_font.render(f"Mode 3: Tracking", True, blue)
text_exit = text_font.render(f"Exit", True, red)

#Setting initial joystick number and intializing all josticks
a=1
joysticks = [joystick1,joystick2,joystick3,joystick4,joystick5]


while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Handle user input and update velocity
    if a ==1 or a==3 or a==4:
        y_inputs = joysticks[a-1].read_x()
        x_inputs = joysticks[a-1].read_y()

        box_vel_y += x_inputs*-100
        box_vel_x += y_inputs*100
    elif a ==5:
        y_inputs = joysticks[a-1].read_x()
        x_inputs = joysticks[a-1].read_y()

        box_vel_y += y_inputs*100
        box_vel_x += x_inputs*-100
    else:
        a = 1

    box_vel_x *= 0.1
    box_vel_y *= 0.1

    # Update box position
    box_x += box_vel_x
    box_y += box_vel_y

    if box_x < 0:
        box_x = 0
    elif box_x > WINDOW_WIDTH - BOX_WIDTH:
        box_x = WINDOW_WIDTH - BOX_WIDTH
    if box_y < 0:
        box_y = 0
    elif box_y > WINDOW_HEIGHT - BOX_HEIGHT:
        box_y = WINDOW_HEIGHT - BOX_HEIGHT

    # Check if box is overlapping with any station
    if station1_rect.colliderect(pygame.Rect(box_x, box_y, BOX_WIDTH, BOX_HEIGHT)):
        # Show prompt for station 1
        pygame.mixer.music.pause()
        print("You have reached station 1!")
        subprocess.call(["python", station1_action])
        pygame.mixer.music.unpause()
        box_x = WINDOW_WIDTH // 2
        box_y = WINDOW_HEIGHT // 2
        highscores = update_highscores()
    elif station2_rect.colliderect(pygame.Rect(box_x, box_y, BOX_WIDTH, BOX_HEIGHT)):
        # Show prompt for station 2
        pygame.mixer.music.pause()
        print("You have reached station 2!")
        subprocess.call(["python", station2_action])
        pygame.mixer.music.unpause()
        box_x = WINDOW_WIDTH // 2
        box_y = WINDOW_HEIGHT // 2
        highscores = update_highscores()
    elif station3_rect.colliderect(pygame.Rect(box_x, box_y, BOX_WIDTH, BOX_HEIGHT)):
        # Show prompt for station 3
        pygame.mixer.music.pause()
        print("You have reached station 3!")
        subprocess.call(["python", station3_action])
        pygame.mixer.music.unpause()
        box_x = WINDOW_WIDTH // 2
        box_y = WINDOW_HEIGHT // 2
        highscores = update_highscores()
    elif exit_rect.colliderect(pygame.Rect(box_x, box_y, BOX_WIDTH, BOX_HEIGHT)):
        # Show prompt for exit
        print("You have reached the exit!")
        pygame.quit()
        sys.exit()
    # Draw objects
    screen.blit(background, (0, 0))
    screen.blit(station1_img, (station1_rect.x, station1_rect.y))
    screen.blit(station2_img, (station2_rect.x, station2_rect.y))
    screen.blit(station3_img, (station3_rect.x, station3_rect.y))
    screen.blit(exit_img, (exit_rect.x, exit_rect.y))
    if box_vel_x < 0:
        screen.blit(inverted_box_img, (box_x, box_y))
    else:
        screen.blit(box_img, (box_x, box_y))
    screen.blit(text_header, (WINDOW_WIDTH-text_header.get_width()-30, 0))
    screen.blit(text_st1, (WINDOW_WIDTH-text_st1.get_width()-30, text_header.get_height()))
    screen.blit(text_st2, (WINDOW_WIDTH-text_st2.get_width()-30, text_st1.get_height()+text_header.get_height()))
    screen.blit(text_st3, (WINDOW_WIDTH-text_st3.get_width()-30, text_st2.get_height()+text_st1.get_height()+text_header.get_height()))
    screen.blit(text_exit, (exit_rect.x+15, exit_rect.y-text_exit.get_height()))
    screen.blit(text_station1, (station1_rect.x-45, station1_rect.y-text_station1.get_height()))
    screen.blit(text_station2, (station2_rect.x-45, station2_rect.y-text_station2.get_height()))
    screen.blit(text_station3, (station3_rect.x-45, station3_rect.y-text_station3.get_height()))
    
    # Update display and tick clock
    pygame.display.update()
    clock.tick(60)
