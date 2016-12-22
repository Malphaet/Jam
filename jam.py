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
GREEN = (50,255,50)
GREY = (210, 210 ,210)
BLUE=(64, 119, 178)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)

# Classes
class GameCar(pygame.sprite.Sprite):
	def __init__(self, ncar):
		pygame.sprite.Sprite.__init__(self)
		self.car=ncar
		self.drawcar()

	def drawcar(self):
		self.image = pygame.Surface([self.car.width, self.car.height])
		self.image.fill(WHITE)
		self.image.set_colorkey(WHITE)
		pygame.draw.rect(self.image, self.car.color, [0, 0, self.car.width, self.car.height])
		self.rect = self.image.get_rect()
		self.original=self.image

	def movecar(self):
		self.image=pygame.transform.rotate(self.original,180-self.car.theta)
		self.x,self.y=self.car.ax,self.car.ay
		self.rect = self.image.get_rect()
		self.rect.center=self.x,self.y

	def update(self):
		self.movecar()
		self.car.update()

class Car (object):
	def __init__(self,lane,pos,max_speed):
		"General init for a car"
		self.theta,self.r=pos*5,lane2r(lane)
		self.secu=2
		self.x,self.y=0,0
		self.speed=0
		self.lane=lane
		self.max_speed=max_speed
		self.pos=pos
		self.secdist=0
		self.prev_car=None
		self.acc=self.accelerate()
		self.apply()
		self.color=(random.randint(0,255),random.randint(0,255),random.randint(0,255))
		self.width,self.height=random.randint(5,15),random.randint(10,20)
	
	def accelerate(self):
		"Not sure about this one"
		return random.randint(3,4)
	
	def setup(self,car,car_list):
		"Link every car with the previous one"
		self.drawcar=car
		if self.pos+1==len(car_list):
			self.prev_car=car_list[0]
		else:
			self.prev_car=car_list[self.pos+1]
		self.secdist=(self.height+self.prev_car.height)/2

	def pickspeed(self):
		"Picks a speed for the current frame"
		dist=self.dist()
		if self.emergency(dist):
			return
		if dist<self.speed*self.secu:
			self.speed-=self.acc
			if self.speed<0:
				self.speed=0
		if self.speed<self.max_speed:
			self.speed+=self.acc
		else:
			self.speed=self.max_speed
		
	def move(self):
		"Moving the car by the decided number of degrees, emergency must be called and handled before"
		Da=self.speed*1./FRAMERATE
		nT=Da+self.theta
		self.theta=nT
		self.theta%=360
			
	def dist(self):
		"Gives the wanabe likely correct distance between the two cars"
		delt=self.prev_car.theta-self.theta
		if delt<-50:
			delt+=360
		return math.pi*self.r*delt/180
	
	def emergency(self,dist):
		"Emergency break in case of imminent collision"
		if dist<self.secdist:
			self.speed-=5*self.acc
			if self.speed<0:
				self.speed=0
				return True
		return False

	def apply(self):
		"Changes the car's carthesian coordinates"
		self.x=int(math.cos(self.theta/180.*math.pi)*self.r)
		self.y=int(math.sin(self.theta/180.*math.pi)*self.r)
		self.ax,self.ay=self.x+CENTER[0],self.y+CENTER[1]

	def update(self):
		"The course of functions that will be used every times the car is updated"
		#print "Cat {} updated".format(self.pos)
		self.pickspeed()
		self.move()
		self.apply()

	def __str__(self):
		return "Car{} lane:{} ({:2d},{:2d}) - ({:2d}°,{:2d})".format(self.pos,self.lane,self.x,self.y,self.theta,self.r)
	
class BrokenCar(Car):
	def __init__(self,lane,pos,max_speed,jam=20):
		Car.__init__(self,lane,pos,max_speed)
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
			self.acc=self.accelerate()
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

class Mouducul(Car):
	def __init__(self,lane,pos,max_speed,reacttime=2):
		Car.__init__(self,lane,pos,max_speed)
		self.color=GREEN
		self.timeel=0
		self.slack=0
		self.timespent=0
		self.reacttime=int(reacttime*FRAMERATE)
		self.apply()

	def update(self):
		self.slackspeed()
		self.move()
		self.apply()

	def slackspeed(self):
		if self.timeel>0:
			self.timeel-=1
			self.timespent+=1
		else:
			self.pickspeed()
			if self.speed==0:
				self.color=(50,max(0,255-self.timespent*2),50)
				self.drawcar.drawcar()
				self.drawcar.movecar()
				self.slack=1
				self.timeel=random.randint(1,10)*self.reacttime/10
			else:
				self.timespent=0
				self.color=GREEN
				self.drawcar.drawcar()
				self.drawcar.movecar()
class CarList (object):
	def __init__(self):
		pass

def lane2r(lane):
	return lane*20+70

def distsec(lane,vmax):
	"The angle/s max according to the dist in px/s picked" 
	return vmax*1.*FRAMERATE/lane2r(lane)
# Init
lanes=[]

cars=[Mouducul]*8+[BrokenCar]*0+[Car]*0
nbtcar=len(cars)

screen = pygame.display.set_mode(SCREENSIZE)
pygame.display.set_caption("Car Jam")
all_sprites_list = pygame.sprite.Group()

for j in xrange(1,16):
	carlist=[]
	sprite=[]
	for i in xrange(7+j*5):
		CT=cars[random.randint(0,nbtcar-1)]
		ncar=CT(j,i,distsec(j,100))
		carlist+=[ncar]
		c = GameCar(ncar)
		c.rect.x = ncar.ax
		c.rect.y = ncar.ay
		sprite+=[c]
		all_sprites_list.add(c)
	lanes+=[carlist]

	for i in xrange(len(carlist)):
		c=carlist[i]
		dc=sprite[i]
		c.setup(dc,carlist)

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
