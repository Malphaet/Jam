#!/usr/bin/env python
#-*- coding:utf-8 -*-

# Import
import pygame, math, sys, random
from pygame.locals import *

# CONSTS
SCREENSIZE=(1024, 768)
screen = pygame.display.set_mode(SCREENSIZE)
clock = pygame.time.Clock()
FRAMERATE=30
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
		self.theta,self.r=pos*15,lane*40+80
		self.secu=2
		self.x,self.y=0,0
		self.speed=0
		self.lane=lane
		self.max_speed=max_speed
		self.pos=pos
		self.prev_car=None
		self.acc=random.randint(1,10)
		self.apply()
		self.color=(random.randint(0,255),random.randint(0,255),random.randint(0,255))
		self.width,self.height=random.randint(5,15),random.randint(10,20)

	def setup(self,car_list):
		if self.pos+1==len(car_list):
			self.prev_car=car_list[0]
		else:
			self.prev_car=car_list[self.pos+1]
	def pickspeed(self):
		dist=self.dist()
		if dist<max(self.speed*self.secu,self.height*2):
			self.speed-=self.acc
			if self.speed<0:
				self.speed=0
		else:
			if self.speed<self.max_speed:
				self.speed+=self.acc
			else:
				self.speed=self.max_speed
	def move(self):
		#Moving
		Da=self.speed*1./FRAMERATE
		nT=Da+self.theta
		if nT>=self.prev_car.theta:
			print "Crash {}".format(self.pos)
		self.theta=nT
		self.theta%=360
			
	def dist(self):
		delt=self.prev_car.theta-self.theta
		if delt<-50:
			delt+=360
		return math.pi*self.r*delt/180
	
	def apply(self):
		self.x=int(math.cos(self.theta/180.*math.pi)*self.r)
		self.y=int(math.sin(self.theta/180.*math.pi)*self.r)
		self.ax,self.ay=self.x+CENTER[0],self.y+CENTER[1]

	def update(self):
		#print "Cat {} updated".format(self.pos)
		self.pickspeed()
		self.move()
		self.apply()

	def __str__(self):
		return "Car{} lane:{} ({:2d},{:2d}) - ({:2d}°,{:2d})".format(self.pos,self.lane,self.x,self.y,self.theta,self.r)
	
class BrokenCar(Car):
	def __init__(self,lane,pos,max_speed,jam=20):
		Car.__init__(self,lane,pos,max_speed*2/3)
		self.color=RED
		self.stuck=0
		self.time=0
		self.immune=0
		self.jam=jam
		self.apply()

	def update(self):
		self.pickspeed()
		self.move()
		self.slack()
		self.apply()
	def slack(self):
		if self.stuck==0:
			self.acc=5
			if self.immune<0 and random.randint(0,100)<self.jam:
				self.stuck=1
				self.time=random.randint(1,6)*FRAMERATE/6
			else:
				self.immune-=1

		else:
			self.speed=0
			self.acc=0
			self.time-=1
			if self.time<0:
				self.stuck=0
				self.immune=FRAMERATE*4


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
	for i in xrange(10+j*3):
		CT=Car
		if i%3==0:
			CT=BrokenCar
		ncar=CT(j,i,10*j)
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

		clock.tick(FRAMERATE)

pygame.quit()
