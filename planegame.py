# coding=utf-8

import os, sys
import pygame
from pygame.locals import *
from gameobj import *
import random

if not pygame.font: print ('Warning, fonts disabled')
if not pygame.mixer: print ('Warning, sound disabled')

# SCREEN_WIDTH = 480
# SCREEN_HEIGHT = 700

# initialization 
pygame.init() # initializes modules
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT)) # create a graphical window, set size
pygame.display.set_caption('Thunder Fighter ') # set title of window

# load background image 
background_img = pygame.image.load('data\\img\\background.png')
background_img_rect = background_img.get_rect()

# load game over image 
game_over_img = pygame.image.load('data\\img\\gameover.png')
game_over_img_rect = game_over_img.get_rect()

# load shoot image 
shoot = pygame.image.load('data\\img\\shoot.png')

# load game sound 
bullet_sound = pygame.mixer.Sound('data\\audio\\bullet.wav')
enemy1_down_sound = pygame.mixer.Sound('data\\audio\\enemy1_down.wav')
enemy2_down_sound = pygame.mixer.Sound('data\\audio\\enemy2_down.wav')
enemy3_down_sound = pygame.mixer.Sound('data\\audio\\enemy3_down.wav')
game_music_sound = pygame.mixer.music.load('data\\audio\\game_music.wav')
game_over_sound = pygame.mixer.Sound('data\\audio\\game_over.wav')

bullet_sound.set_volume(0.3)
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.2)

hero_rects = []
hero_rects.append(pygame.Rect(165, 360, 102, 126)) # hero2
hero_rects.append(pygame.Rect(165, 234, 102, 126)) # hero_blowup_n1

hero_pos = [189, 500] # setting of player
hero = Hero(shoot, hero_rects, hero_pos) # generate a hero object 

# bullet picture 
bullet_rect = pygame.Rect(1004, 987, 9, 21)
bullet_img = shoot.subsurface(bullet_rect)

# enemy image 
enemy1_rect = pygame.Rect(534, 612, 57, 43)
enemy1_img = shoot.subsurface(enemy1_rect)

# enemy boom 
enemy1_down_imgs = []
enemy1_down_imgs.append(shoot.subsurface(pygame.Rect(267, 347, 57, 51))) # enemy1_down1

# enemy object 
enemies1 = pygame.sprite.Group()

# enemy dead object 
enemies_down = pygame.sprite.Group()

shot_frequency = 0 # shot frequency 
enemy_frequency = 0 # enemy frequency 
hero_down_index = 2 # hero down index 
score = 0 # score 

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

	# control FPS 
	pygame.time.Clock().tick(60)

	# shoot bullet 
	if not hero.is_hit:
		if shot_frequency % 15 == 0:
			bullet_sound.play() # play sound 
			hero.shoot(bullet_img) # shoot 
		shot_frequency += 1
		if shot_frequency >= 15:
			shot_frequency = 0
	
	# generate enemy 
	if enemy_frequency % 50 == 0:
		enemy1_pos = [random.randint(0, SCREEN_WIDTH - enemy1_rect.width),0] # enemy location 
		enemy1 = Enemy(enemy1_img, enemy1_down_imgs, enemy1_pos)
		enemies1.add(enemy1) # append to enemy list 
	enemy_frequency += 1
	if enemy_frequency > 50:
		enemy_frequency = 0

	# move bullet 
	for bullet in hero.bullets:
		bullet.move()
		if bullet.rect.top < 0:
			hero.bullets.remove(bullet)
	
	# move enemy 
	for enemy1 in enemies1:
		enemy1.move()

		# judge whether they crash 
		if pygame.sprite.collide_circle(enemy1, hero):
			enemies_down.add(enemy1) # add to down 
			enemies1.remove(enemy1)  # remove from enemy list 
			hero.is_hit = True
			game_over_sound.play()
			pygame.mixer.music.stop()
			running = False  
			break
		if enemy1.rect.top > SCREEN_HEIGHT:
			enemies1.remove(enemy1)

	collisions = pygame.sprite.groupcollide(enemies1, hero.bullets, 1, 1)
	for enemy_down in collisions:
		enemies_down.add(enemy_down)
		score += 10


	# plot background
	screen.fill(0)
	screen.blit(background_img,background_img_rect)
	
	# plot hero
	if not hero.is_hit:
		screen.blit(hero.image[hero.img_index], hero.rect)
		hero.img_index += 1
		if hero.img_index >=2 :
			hero.img_index = 0


	# bullets and enemy
	hero.bullets.draw(screen)
	enemies1.draw(screen)

	# score 
	score_font = pygame.font.Font('data\\font\\CHILLER.TTF', 36)
	score_text = score_font.render(str(score), True, (240, 0, 87)) # get a new surface
	score_text_rect = score_text.get_rect()
	screen.blit(score_text,score_text_rect)
	
	# update screen 
	pygame.display.update()
	key_pressed = pygame.key.get_pressed()
	if not hero.is_hit:
		if key_pressed[K_UP] or key_pressed[K_w]:
			hero.moveUp()
		if key_pressed[K_DOWN] or key_pressed[K_s]:
			hero.moveDown()
		if key_pressed[K_LEFT] or key_pressed[K_a]:
			hero.moveLeft()
		if key_pressed[K_RIGHT] or key_pressed[K_d]:
			hero.moveRight()

screen.blit(game_over_img, game_over_img_rect)
pygame.display.update()
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()


