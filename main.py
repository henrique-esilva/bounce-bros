#! python3.8

import os, sys

dirpath = os.getcwd()
sys.path.append(dirpath)

if getattr(sys, "frozen", False):
    os.chdir(sys._MEIPASS)

import pygame
from pygame.locals import *
import betatest



pygame.init()
pygame.font.init()
#pygame.mixer.init()


font_consolas = pygame.font.Font(pygame.font.match_font('consolas'), 18)

def void_function(): pass
def set_arrow_control():
    betatest.controle_adequado_efetivo = betatest.controle_adequado_efetivo2
    menu.options[1] = 'Control with: Arrows'
    menu.functions[1] = set_wasd_control
def set_wasd_control():
    betatest.controle_adequado_efetivo = betatest.controle_adequado_efetivo1
    menu.options[1] = 'Control with: WASD'
    menu.functions[1] = set_arrow_control

class GeneralGameControl():
    state = 'menu'

    def gotogame(self):
        self.state = 'game'

game_control = GeneralGameControl()

class MenuModel():
    options = ['Play', 'Control with: WASD']
    functions = [game_control.gotogame, set_arrow_control]
    time_stop = 0
    max_time_stop = 5
    state = 'menu'

    def reduce_time_stop(self):
        if self.time_stop > 0: self.time_stop -= 1
    def reset_time_stop(self):
        self.time_stop = self.max_time_stop
    def gts(self):
        return self.time_stop

keys = None
menu = MenuModel()
selected_option = 0


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    pygame.time.Clock().tick(40)

    keys = pygame.key.get_pressed()

    if game_control.state == 'menu':
        menu.reduce_time_stop()
        if not menu.gts() and keys[K_UP]: selected_option -= 1; menu.reset_time_stop()
        if not menu.gts() and keys[K_DOWN]: selected_option += 1; menu.reset_time_stop()

        if selected_option < 0: selected_option = 0
        if selected_option > len(menu.options)-1: selected_option = len(menu.options)-1

        if not menu.gts() and keys[K_RETURN]:
            menu.functions[selected_option](); menu.reset_time_stop()
        
        pygame.draw.circle(betatest.renderiza.pre_tela, (255,255,255), (10, (selected_option*20)+10), 3)
        for op in range(len(menu.options)):
            betatest.renderiza.pre_tela.blit(
                font_consolas.render(menu.options[op], False, betatest.renderiza.color.colorWhite, betatest.renderiza.color.colorGrey),
                Rect(20, 20*op, 0, 0)
            )
        betatest.renderiza.renderiza_tela()

    if game_control.state == 'game':
        betatest.main()
