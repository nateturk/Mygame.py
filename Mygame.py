# This file was created by Nate Turkington
# Source: http://kidscancode.org/blog/
 
# import libraries and modules
from typing import Self
import pygame as pg
from pygame.sprite import Sprite
import random
from random import randint
import os
from settings import *
from sprites import *
import math
 
# Goals:
# Create a scoring system that gives you points the higher you go
# Whenever the player moves all the way to the end of the map on either the left or right side, the player ends up on the opposite side
# Have the map move up as the player moves up the platforms
# Make moving platforms
 
vec = pg.math.Vector2
 
# Images and sounds are imported here
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')
snd_folder = os.path.join(game_folder, 'sounds')
 
class Game:
   def __init__(self):
       # init pygame and create a window
       pg.init()
       pg.mixer.init()
       self.screen = pg.display.set_mode((WIDTH, HEIGHT))
       pg.display.set_caption("My Game...")
       self.clock = pg.time.Clock()
       self.running = True
       self.font_name = pg.font.match_font('arial')
   
   def new(self):
       # create a group for all sprites
       self.score = 0
       self.all_sprites = pg.sprite.Group()
       self.all_platforms = pg.sprite.Group()
       self.all_mobs = pg.sprite.Group()
       # instantiate classes
       self.player = Player(self)
       # add instances to groups
       self.all_sprites.add(self.player)
 
       for p in PLATFORM_LIST:
           # instantiation of the Platform class
           plat = Platform(*p)
           self.all_sprites.add(plat)
           self.all_platforms.add(plat)
 
       for m in range(0,10):
           m = Mob(randint(0, WIDTH), randint(0, math.floor(HEIGHT/2)), 20, 20, "normal")
           self.all_sprites.add(m)
           self.all_mobs.add(m)
 
       self.run()
   
   def run(self):
       self.playing = True
       while self.playing:
           self.clock.tick(FPS)
           self.events()
           self.update()
           self.draw()
 
   def update(self):
       self.all_sprites.update()
 
       # prevents the player from falling through the platform when falling down...
       if self.player.vel.y >= 0:
           hits = pg.sprite.spritecollide(self.player, self.all_platforms, False)
           if hits:
               self.player.pos.y = hits[0].rect.top
               self.player.vel.y = 0
               self.player.vel.x = hits[0].speed*1.5
       
                   
        # prevents player from jumping up through a platform
       elif self.player.vel.y <= 0:
           hits = pg.sprite.spritecollide(self.player, self.all_platforms, False)
           if hits:
               self.player.acc.y = 5
               self.player.vel.y = 0
               print("bruh")
               self.score -= 1
               if self.player.rect.bottom >= hits[0].rect.top - 1:
                   self.player.rect.top = hits[0].rect.bottom
      
       # advance screen
       if self.player.rect.top <= HEIGHT / 4:
           self.player.pos.y += abs(self.player.vel.y)
           for plat in self.all_platforms: 
               plat.rect.y += abs(self.player.vel.y)
               if plat.rect.top >= HEIGHT:
                   plat.kill()
                   self.score += 10
 
       # ends game
       if self.player.rect.bottom > HEIGHT:
           for sprite in self.all_sprites:
               sprite.rect.y -= max(self.player.vel.y, 10)
               if sprite.rect.bottom < 0:
                   sprite.kill()
       if len(self.all_platforms) == 0:
           self.playing = False
 
       #spawn platforms
       while len(self.all_platforms) < 6: 
           width = random.randrange(50,100)
           p = Platform(random.randrange(0, WIDTH - width),
                        random.randrange(-75, -30),
                        width, 20, "moving")
           self.all_platforms.add(p)
           self.all_sprites.add(p)
 
       # player wraps around screen
       if self.player.pos.x > WIDTH: 
           self.player.pos.x = 0
       if self.player.pos.x < 0: 
           self.player.pos.x = WIDTH
 
   def events(self):
       for event in pg.event.get():
       # check for closed window
           if event.type == pg.QUIT:
               if self.playing:
                   self.playing = False
               self.running = False
               
   def draw(self):
       ############ Draw ################
       # draw the background screen
       self.screen.fill(BLACK)
       # draw all sprites
       self.all_sprites.draw(self.screen)
       self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH/2, HEIGHT/10)
       # buffer - after drawing everything, flip display
       pg.display.flip()
 
   def show_start_screen(self):
       pass
 
   def show_go_screen(self):
       pass    
   
   def draw_text(self, text, size, color, x, y):
       font = pg.font.Font(self.font_name, size)
       text_surface = font.render(text, True, color)
       text_rect = text_surface.get_rect()
       text_rect.midtop = (x, y)
       self.screen.blit(text_surface, text_rect)
 
# make platforms move
PLATFORM_LIST = [(0, HEIGHT - 40, WIDTH, 40, "normal"),
                (WIDTH / 2 - 50, HEIGHT * 3 / 4, 250, 20,"moving"),
                (125, HEIGHT - 200, 100, 20, "moving"),
                (292, 200, 100, 20, "moving"),
                (75, 100, 50, 20, "moving")]
 
g = Game()
g.show_start_screen()
while g.running:
   g.new()
   g.show_go_screen()
 
pg.quit()