import pygame, sys, os
from pygame.locals import *
import betatest



pygame.init()





while True:
    for i in pygame.event.get():
        if i.type == pygame.QUIT: sys.exit()

    betatest.main()
