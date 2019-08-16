import pygame
import sys
import math
import time
from collections import OrderedDict

def line_above(x,y, pt1, pt2):
    return y - pt1[1] > (pt2[1]-pt1[1])/(pt2[0]-pt1[0])*(x-pt1[0])

class BoardGui:
    def __init__(self, tile, action_bar, screen):
        self.action_bar = action_bar.convert_alpha()
        self.tile = tile.convert_alpha()
        self.tile_rect = tile.get_rect()
        print(self.tile_rect.center)
        self.screen = screen
        self.coord = {} 
        self.coord_center = {}
        self.coord_end = {}
        self.tw, self.th = tile.get_size()
        self.tile_y_offset = self.th//2
        self.tile_x_offset = self.tw//2
        self.screen_w, self.screen_h = self.screen.get_size()
        self.font = pygame.font.Font('freesansbold.ttf',15)
        self.x_lines = {}
        self.y_lines = {}
        for y in range(0, 11):
            for x in reversed(range(0, 11)):
                if x == 0 and (y > 8 or y < 2):
                    continue
                if x == 1 and (y > 9 or y < 1):
                    continue
                if x == 9 and (y > 9  or y < 1):
                    continue
                if x == 10 and (y > 8 or y < 2):
                    continue
                self.coord[(x,y)] = self.get_real_xy(x, y)
        self.coord_grid = self.create_grid(self.coord.copy())

        print(len(self.coord))
        self.coord = OrderedDict(sorted(self.coord.items(),key=lambda
                                        x:x[0][1]))
        for k, v in self.coord_grid.items():
            self.coord_center[k]=(v[0]+self.tile_rect.center[0]
            ,v[1]+self.tile_rect.center[1])
            self.coord_end[k]=(v[0]
            ,v[1]+self.th//2)
        

        print(self.coord)
  
    def create_grid(self, coord):
        coord[(2,11)] = self.get_real_xy(2,11)
        coord[(7,11)] = self.get_real_xy(7,11)
        coord[(11,2)] = self.get_real_xy(11,2)
        coord[(11,7)] = self.get_real_xy(11,7)
        
        return coord

    def get_real_xy(self, x, y):
        theta = -math.pi/4-.0001
        x *= self.tw *.580
        y *= self.th * .9 
        tx = int((x * math.cos(theta) - y * math.sin(theta))*1.25)-100
        ty = int((y * math.cos(theta) + x * math.sin(theta))*.78) + 600 
        return (tx, ty)
    
    def draw_lines(self):
        for y in range(0,12):
            pygame.draw.line(self.screen, (123,0,43), self.coord_end[(2,y)],
                                                                 self.coord_end[(7,y)])
            pygame.draw.line(self.screen, (123,0,43), self.coord_end[(y,2)],
                                                                 self.coord_end[(y,7)])
 
            self.x_lines[y] = [self.coord_end[(2,y)], self.coord_end[(7,y)]]
            self.y_lines[y] = [self.coord_end[(y,2)], self.coord_end[(y,7)]]

    def draw_tiles(self):
        for k, v in self.coord.items():
            self.screen.blit(self.tile, v)
            text = self.font.render(str(k), True, (123,0,43))
            
            self.screen.blit(text, self.coord_center[k])
    
    def draw_board(self):
        self.draw_tiles()
        self.draw_actionbar()
        self.draw_lines() 
    
    def draw_actionbar(self):
        self.screen.blit(self.action_bar, (self.screen_w-500, 25))
    def get_tile(self, x, y):
        tile_x, tile_y = None, None
        for i in range(0,12):
            pt1, pt2 = self.x_lines[i]
            if line_above(x,y, pt1, pt2):
                tile_y = i
                continue
        for i in reversed(range(0,12)):
            pt1, pt2 = self.y_lines[i]
            if line_above(x, y, pt1, pt2):
                tile_x = i
                continue
        try: 
            if (tile_x-1, tile_y) in self.coord:
                return tile_x-1, tile_y
        except:
            pass
        return None
pygame.init()
tile_path = 'sprites/board/tile.png'
screen = pygame.display.set_mode((1700,1200))

tile = pygame.image.load(tile_path)
action_bar = pygame.image.load('sprites/board/action_bar_icon.png')
b = BoardGui(tile, action_bar, screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print('In the event loop:', event.pos, event.button)
            print('tile clicked: ', b.get_tile(event.pos[0],event.pos[1]))
    screen.fill((0,0,0))
    b.draw_board()
    pygame.display.flip()
