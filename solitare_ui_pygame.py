import numpy as np
import time
import pygame
from solitare_game import solitare
from xarm.wrapper import XArmAPI
import ipywidgets as widgets
from IPython.display import display

test = widgets.Text(value='Hello World!', disabled=True)
display(test)

pygame.init()
screen = pygame.display.set_mode((1280, 720), pygame.SCALED)
running = True
pygame.display.set_caption("Solitare with a very expensive robot arm")
#arm = XArmAPI(port='127.0.0.1')
#game = solitare(arm=arm)
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((200, 200, 200))
screen.blit(background, (0, 0))
pygame.display.flip()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background, (0, 0))
    pygame.display.flip()

    

    
