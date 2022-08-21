import os, sys
import pygame
from pygame.locals import *

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 700

# Bullet Class 
class Bullet(pygame.sprite.Sprite):
	def __init__(self, bullet_img, init_pos):
		super(Bullet, self).__init__()
		self.image = bullet_img 				 		# set bullet image
		self.rect = self.image.get_rect() 		 		# get coordinate of bullet
		self.rect.midbottom = init_pos 			 		# set initial position
		self.speed = 10 						 		# set speed of bullet

	def move(self):
		self.rect.top -= self.speed

# Hero Class
class Hero(pygame.sprite.Sprite):
	def __init__(self, shoot, hero_rects, init_pos):
		super(Hero, self).__init__()
		self.image = [] 						 		# picture list of different 
		for i in range(len(hero_rects)):
			self.image.append(shoot.subsurface(hero_rects[i]).convert_alpha()) # fill the list
			self.rect = hero_rects[0] 			 		# get the hero x,y axis 
			self.rect.topleft = init_pos    	 		# initialization position 
			self.speed = 10 					 		# setting of player speed
			self.bullets = pygame.sprite.Group() 		# bullet group 
			self.img_index = 0
			self.is_hit = False

	def shoot(self, bullet_img):
		bullet = Bullet(bullet_img, self.rect.midtop) 	# generate bullet
		self.bullets.add(bullet) 						# add to the bullet group 

	def moveUp(self):
		if self.rect.top <= 0:
			self.rect.top = 0
		else:
			self.rect.top -=self.speed

	def moveDown(self):
		if self.rect.top >= SCREEN_HEIGHT - self.rect.height:
			self.rect.top = SCREEN_HEIGHT - self.rect.height
		else:
			self.rect.top += self.speed

	def moveLeft(self):
		if self.rect.left <= 0:
			self.rect.left = 0
		else:
			self.rect.left -= self.speed

	def moveRight(self):
		if self.rect.left >= SCREEN_WIDTH - self.rect.width:
			self.rect.left = SCREEN_WIDTH - self.rect.width
		else:
			self.rect.left += self.speed

# Enemy Class
class Enemy(pygame.sprite.Sprite):
	def __init__(self, enemy_img, enemy_down_imgs, init_pos):
		super(Enemy, self).__init__()
		self.image = enemy_img
		self.rect = self.image.get_rect()
		self.rect.topleft = init_pos
		self.enemy_down_img = enemy_down_imgs
		self.speed = 2
		self.down_index = 0

	def move(self):
		self.rect.top += self.speed
