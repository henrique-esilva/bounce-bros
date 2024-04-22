import os, sys

dirpath = os.getcwd()
sys.path.append(dirpath)

if getattr(sys, "frozen", False):
    os.chdir(sys._MEIPASS)

import pygame
from pygame.locals import *
import betatest



pygame.init()
#pygame.mixer.init()





while True:
    for i in pygame.event.get():
        if i.type == pygame.QUIT: sys.exit()

    betatest.main()
