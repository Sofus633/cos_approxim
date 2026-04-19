import sys

import pygame, math, time
from pygame.locals import *

from decimal import Decimal

pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
origin = (width//2, height//2)
zoom_force = 2
precision = 4
cos_derivate = [1, 0, -1, 0]
iterations = 1


def cos_app(x):
    return  1 - ((x*x)/2)

def cos_app_global(x):
    global precision, cos_derivate
    y = 1
    cos_derivate_i = 1
    for i in range(1, precision):
        print(x)
        y += cos_derivate[cos_derivate_i] * (pow(x, i)/math.factorial(i))
        cos_derivate_i += 1
        if cos_derivate_i > 3:
            cos_derivate_i = 0
    return y

#not reallt a vector x-x
class Vector2:
    def __init__(self, x = 0, y = 0, func=math.cos):
        self.x = x;
        self.y = y;
        self.x_scale = 10;
        self.y_scale = 10;
        self.function = func

    def move(self, x, y):
        self.x =  x
        self.y =  y
        self.plot_eq()

    def scale_up(self, x, y):
        return (int(x*self.x_scale) + self.x, int(y*self.y_scale) + self.y)

    def zoom(self, x, y):
        global zoom_force
        if self.x_scale + y > 0 and self.y_scale + y > 0:
            self.x_scale += y * zoom_force
            self.y_scale += y * zoom_force
            self.plot_eq()

    def plot_eq(self):
        global screen, height, width, cos_derivate

        cosrange = iterations * math.pi
        
        pixAr = pygame.PixelArray(screen)
        x = -cosrange
        tmpy = 0 
        while (x < cosrange):


            #tmpy = 1 - ((x*x)/2)
            tmpy = self.function(x)
            #print(f"pixel at  {x}, {tmpy}");
            pixelpos = self.scale_up(x, tmpy)
            #print(f"x={x} y={tmpy}")
            if (pixelpos[1] < height and pixelpos[1] >= 0 and pixelpos[0] < width and pixelpos[0] >= 0):
                pixAr[pixelpos] = int(x*10000) 
                #print(f"pixel at  {pixelpos}")
            x += .012
        pixAr.close()


fps = 60
fpsClock = pygame.time.Clock()





vec1 = Vector2(origin[0], origin[1], cos_app_global)
vec1.plot_eq();


vec2 = Vector2(origin[0], origin[1])
vec2.plot_eq();

pygame.display.flip()


temporigin = (0, 0)
move = 0

while True:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEWHEEL:
            print(f"{event.x, event.y}, {vec1.x_scale, vec1.y_scale}")
            vec1.zoom(event.x, event.y)
            vec2.zoom(event.x, event.y)
            pygame.display.flip()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
            if not move:
                move = 1
                temporigin = (vec1.x, vec1.y)
                mousepos = pygame.mouse.get_pos()
        if event.type == MOUSEBUTTONUP and event.button == 3:
            precision *= 2
            vec1.plot_eq()
            vec2.plot_eq()
            pygame.display.flip()
        if event.type == MOUSEBUTTONUP and event.button == 2:
            move =  0
        if event.type == MOUSEMOTION and move:
            acmousepos = pygame.mouse.get_pos()
            xmov = acmousepos[0] - mousepos[0] + temporigin[0]
            ymov = acmousepos[1] - mousepos[1] + temporigin[1]
            vec1.move(xmov, ymov)
            vec2.move(xmov ,ymov)
            pygame.display.flip()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                iterations += 1
            if event.key == pygame.K_DOWN:
                iterations -= 1
            if event.key in (pygame.K_UP, pygame.K_DOWN):
                vec1.plot_eq()
                vec2.plot_eq()
                pygame.display.flip()
    if (iterations <= 50):
        iterations += 1
        vec1.plot_eq()
        vec2.plot_eq()
        pygame.display.flip()
    fpsClock.tick(fps)

pygame.quit() 
