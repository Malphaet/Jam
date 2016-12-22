#!/usr/bin/env python
#-*- coding:utf-8 -*-

# Import
import pygame, math, sys, random
from pygame.locals import *

# CONSTS
SCREENSIZE=(1024, 768)
screen = pygame.display.set_mode(SCREENSIZE)
clock = pygame.time.Clock()
CENTER=(SCREENSIZE[0]/2,SCREENSIZE[1]/2)
BLACK=(0,0,0)
WHITE = (255, 255, 255)
GREEN = (20, 255, 140)
GREY = (210, 210 ,210)
BLUE=(64, 119, 178)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)

# Classes
class GameCar(pygame.sprite.Sprite):
	def __init__(self, ncar):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([ncar.width, ncar.height])
		self.image.fill(WHITE)
		self.image.set_colorkey(WHITE)
		pygame.draw.rect(self.image, ncar.color, [0, 0, ncar.width, ncar.height])
		self.car=ncar
		self.rect = self.image.get_rect()
		self.original=self.image
	def update(self):
		self.image=pygame.transform.rotate(self.original,180-self.car.theta)
		self.x,self.y=self.car.ax,self.car.ay
		self.rect = self.image.get_rect()
		self.rect.center=self.x,self.y
		self.car.update()

class Car (object):
	def __init__(self,lane,pos,max_speed):
		self.theta,self.r=pos*10,lane*40+80
		self.x,self.y=0,0
		self.speed=0
		self.lane=lane
		self.max_speed=max_speed
		self.pos=pos
		self.prev_car=None
		self.acc=random.randint(1,10)
		self.rotate()
		self.color=(random.randint(0,255),random.randint(0,255),random.randint(0,255))
		self.width,self.height=random.randint(5,15),random.randint(10,20)
	def setup(self,car_list):
		if self.pos+1==len(car_list):
			self.prev_car=car_list[0]
		else:
			self.prev_car=car_list[self.pos+1]
	
	def move(self):
		dist=self.dist()
		if dist<self.speed:
			self.speed-=self.acc
		else:
			if self.speed<self.max_speed:
				self.speed+=self.acc+random.randint(1,3)
			else:
				self.speed=self.max_speed
		
		#Moving
		Da=self.speed*5./self.r
		self.theta+=Da
		self.theta%=360
		self.rotate()
		#print "Car {} is at {}px Delta {}".format(self.pos,dist,Da)
				
	def dist(self):
		delt=self.prev_car.theta-self.theta
		if delt<0:
			delt+=180
		return math.pi*self.r*delt/180
	
	def rotate(self):	
		self.x=int(math.cos(self.theta/180.*math.pi)*self.r)
		self.y=int(math.sin(self.theta/180.*math.pi)*self.r)
		self.ax,self.ay=self.x+CENTER[0],self.y+CENTER[1]
	def update(self):
		#print "Cat {} updated".format(self.pos)
		self.move()

	def __str__(self):
		return "Car{} lane:{} ({:2d},{:2d}) - ({:2d}°,{:2d})".format(self.pos,self.lane,self.x,self.y,self.theta,self.r)
	

class CarList (object):
	def __init__(self):
		pass


# Init
lanes=[]

screen = pygame.display.set_mode(SCREENSIZE)
pygame.display.set_caption("Car Jam")
all_sprites_list = pygame.sprite.Group()

for j in xrange(1,7):
	carlist=[]
	for i in xrange(10):
		ncar=Car(j,i,30+20*j)
		carlist+=[ncar]
		c = GameCar(ncar)
		c.rect.x = ncar.ax
		c.rect.y = ncar.ay
		all_sprites_list.add(c)
	lanes+=[carlist]

	for c in carlist:
		c.setup(carlist)

# Loop
carryOn = True
clock=pygame.time.Clock()

while carryOn:
		for event in pygame.event.get():
		    if event.type==pygame.QUIT:
				carryOn=False
				
		#Game Logic
		all_sprites_list.update()
		screen.fill(BLUE)
		all_sprites_list.draw(screen)

		pygame.display.flip()

		clock.tick(30)

pygame.quit()
