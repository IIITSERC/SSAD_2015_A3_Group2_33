import pygame, sys
from pygame.locals import *
import random

h2if = "heart2.png"
h1if = "heart1.png"
mif = "chibi.png"
lif = "ladder.png"
wif = "wall.png"
fif = "fireball.png"
cif = "coin.png"
dif = "donkey.png"
pif = "princess.png"

pygame.init()

screen = pygame.display.set_mode( (1000,600),0,32)

coin = pygame.image.load(cif).convert_alpha()
coin = pygame.transform.scale(coin,(20,20))

heart1 = pygame.image.load(h1if).convert_alpha()
heart1 = pygame.transform.scale(heart1,(30,30))

heart2 = pygame.image.load(h2if).convert_alpha()
heart2 = pygame.transform.scale(heart2,(30,30))

ladder = pygame.image.load(lif).convert_alpha()
ladder = pygame.transform.scale(ladder,(40,25))

fireball = pygame.image.load(fif).convert_alpha()
fireball = pygame.transform.scale(fireball,(25,25))

mario = pygame.image.load(mif).convert_alpha()
mario = pygame.transform.scale(mario,(30,32))

donkey = pygame.image.load(dif).convert_alpha()
donkey = pygame.transform.scale(donkey,(60,70))

princess = pygame.image.load(pif).convert_alpha()
princess = pygame.transform.scale(princess,(40,50))

wall = pygame.image.load(wif).convert_alpha()
wall = pygame.transform.scale(wall,(20,20))

grey = (139,134,130)
white = (255,255,255)
black = (0,0,0)

gravity = 0.09
coins_total = 10
score = 0
lives = 3
won = 1
count = 0

myfont = pygame.font.SysFont("monospace",25,bold = True)

clock = pygame.time.Clock()

all_sprites_list = pygame.sprite.Group()
fire_list = pygame.sprite.Group()
coins_list = pygame.sprite.Group()
wall_list = pygame.sprite.Group()
ladder_list = pygame.sprite.Group()
ladder_hit_list = pygame.sprite.Group()
heart_list = pygame.sprite.Group()
princess_list = pygame.sprite.Group()

Gameloop = True
reset = True

def create_walls(x,y,n,walls,alls,coins,her_floor):
	temp = 0
	temp1 = 0
	while ( temp < n ):
		wall1 = Block(x+temp*20,y,wall)
		walls.add(wall1)
		alls.add(wall1)
		temp += 1
		if randomize(3) and temp1 < coins_total and not her_floor:
			coin1 = Block(x+temp*20,y-30,coin)
			alls.add(coin1)
			coins.add(coin1)
		temp1 += 1
		

def create_ladders(x,y,walls,alls,ladders,ladders_hit,proper):
	temp = 0
	if proper:
		while ( temp < 4 ):
			ladder1 = Block(x,y+temp*25,ladder)
			ladders.add(ladder1)
			alls.add(ladder1)
			if temp == 0:
				ladders_hit.add(ladder1)
			temp +=1

	else:
		ladder1 = Block(x,y+75,ladder)
		walls.add(ladder1)
		alls.add(ladder1)
		ladder2 = Block(x,y,ladder)
		alls.add(ladder2)


def create_board(walls,alls,coins,ladders,ladders_hit):

	create_walls(160,0,1,walls,alls,coins,True)
	create_walls(160,20,1,walls,alls,coins,True)
	create_walls(160,40,1,walls,alls,coins,True)
	create_walls(160,60,1,walls,alls,coins,True)
	create_walls(160,80,7,walls,alls,coins,True)
	create_walls(360,0,1,walls,alls,coins,True)
	create_walls(360,20,1,walls,alls,coins,True)
	create_walls(360,40,1,walls,alls,coins,True)
	create_walls(360,60,1,walls,alls,coins,True)
	create_walls(340,80,2,walls,alls,coins,True)
	create_walls(0,180,2,walls,alls,coins,False)
	create_walls(80,180,21,walls,alls,coins,False)
	create_walls(540,180,13,walls,alls,coins,False)
	create_walls(0,280,10,walls,alls,coins,False)
	create_walls(300,280,2,walls,alls,coins,False)
	create_walls(440,280,13,walls,alls,coins,False)
	create_walls(740,280,7,walls,alls,coins,False)
	create_walls(200,380,15,walls,alls,coins,False)
	create_walls(540,380,21,walls,alls,coins,False)
	create_walls(120,380,2,walls,alls,coins,False)
	create_walls(740,480,3,walls,alls,coins,False)
	create_walls(0,480,20,walls,alls,coins,False)
	create_walls(440,480,13,walls,alls,coins,False)
	create_walls(0,580,50,walls,alls,coins,False)

	create_ladders(300,79,walls,alls,ladders,ladders_hit,True)
	create_ladders(40,179,walls,alls,ladders,ladders_hit,True)
	create_ladders(500,179,walls,alls,ladders,ladders_hit,True)
	create_ladders(700,279,walls,alls,ladders,ladders_hit,True)
	create_ladders(960,379,walls,alls,ladders,ladders_hit,True)
	create_ladders(500,379,walls,alls,ladders,ladders_hit,False)
	create_ladders(160,379,walls,alls,ladders,ladders_hit,True)
	create_ladders(960,479,walls,alls,ladders,ladders_hit,True)
	create_ladders(700,479,walls,alls,ladders,ladders_hit,False)
	create_ladders(400,479,walls,alls,ladders,ladders_hit,True)

def randomize(n):
	if random.randrange(0,n) == 1:
		return True
	else:
		return False


def collision(temp_list,block,vanish):
	temp = pygame.sprite.spritecollide(block,temp_list,vanish)
	if len(temp) > 0:
		return True
	else:
		return False


class Fireball (pygame.sprite.Sprite):
	def __init__ (self,x,y,image,speed):
		pygame.sprite.Sprite.__init__(self)
		self.x = x
		self.y = y
		self.ladder = 0
		self.speed = speed
		self.image = image
		self.glide = False
		self.touch = False
		self.wieght = 0
		self.render()

	def render(self):
		self.rect = self.image.get_rect()
		self.rect.x = self.x
		self.rect.y = self.y

	def update(self,walls,ladders,players):
		global lives
		global Gameloop
		global score
		global won
		self.ladder = 3 + (won*2)
		self.wieght += gravity
		self.rect.x += self.speed

		if collision(players,self,True):
			lives -= 1
			Gameloop = False
			score -= 25
			
		ladder_list = pygame.sprite.spritecollide(self,ladders,False)
		if len(ladder_list) > 0 and not self.touch:
			self.glide = randomize(2)
			self.touch = True

		if len(ladder_list) < 1 :
			self.touch = False

		if self.touch and self.glide:
			self.wieght = 0
			self.ladder = 0

		self.rect.y += self.ladder + self.wieght
		
		block_hit_list = pygame.sprite.spritecollide(self,walls,False)
		for block in block_hit_list:
			if self.rect.y < block.rect.y:
				self.rect.bottom = block.rect.top
				self.wieght = 0
				break
		self.check_bounds()

	def check_bounds (self):
		if self.rect.x < 0 : 
			self.rect.x = 0
			self.speed = -1*self.speed
		if self.rect.x > 970 : 
			self.rect.x = 970
			self.speed = -1*self.speed

class Block (pygame.sprite.Sprite):

	def __init__ (self,x,y,image):
		pygame.sprite.Sprite.__init__(self)
		self.x = x
		self.y = y
		self.image = image
	    	self.render()	

	def render(self):
		self.rect = self.image.get_rect()
		self.rect.x = self.x
		self.rect.y = self.y

class Spawn (Block):

	def update(self,fires):
		fire_list = pygame.sprite.spritecollide(self,fires,True)
	
class Player (pygame.sprite.Sprite):

	def __init__ (self,x,y,image):
		pygame.sprite.Sprite.__init__(self)
		self.x = x
		self.y = y
		self.jump_y = 0
		self.ladder_y = 0
		self.wieght = 0
		self.color = color
		self.change_x = 0
		self.change_y = 0
		self.image = image
		self.render()
	
	def move (self,x):
		self.change_x = x

	def ladder (self,y):
		self.ladder_y = y
	
	def jump (self,y = 0):
		self.jump_y = y

	def ladder (self,y):
		self.ladder_y = y 

	def update(self,walls,ladders,coins,damsels):
		global score
		global Gameloop
		global won
		global reset
		self.wieght += gravity
		self.rect.x += self.change_x

		ladder_list = pygame.sprite.spritecollide(self,ladders,False)
	        for ladder in ladder_list:    
			self.wieght = 0 

		rescued = pygame.sprite.spritecollide(self,damsels,False)
		for people in rescued:
			Gameloop = False
			won += 1
			score += 100
			reset = True

		coin_list = pygame.sprite.spritecollide(self,coins,True)
		for coin in coin_list:
			score = score + 5

		block_hit_list = pygame.sprite.spritecollide(self,walls,False)
		for block in block_hit_list:
			if self.change_x > 0:
				self.rect.right = block.rect.left
			else:
				self.rect.left = block.rect.right
		self.rect.y += self.jump_y + self.wieght + self.ladder_y
		block_hit_list = pygame.sprite.spritecollide(self,walls,False)
		for block in block_hit_list:
			if self.wieght + self.jump_y + self.ladder_y > 0:
				self.rect.bottom = block.rect.top
				self.wieght = 0
			else :
				self.rect.top = block.rect.bottom
			break

		self.check_bounds()

	def render(self):
	        self.rect = self.image.get_rect()
	 	self.rect.x = self.x
		self.rect.y = self.y

	def check_bounds (self):
		if self.rect.x < 0 : self.rect.x = 0
		if self.rect.y < 0 : self.rect.y = 0
		if self.rect.x > 970 : self.rect.x = 970
		if self.rect.y > 570 : self.rect.y = 570


class DonkeyKong (pygame.sprite.Sprite):
	def __init__ (self,x,y,image,speed):
		pygame.sprite.Sprite.__init__(self)
		self.x = x
		self.y = y
		self.image = image
		self.speed = speed
	 	self.render()

	def render(self):
		self.rect = self.image.get_rect()
		self.rect.x = self.x
		self.rect.y = self.y

	def check_bounds(self,walls):
		if self.rect.x < 0:
			self.rect.x = 0
		        self.speed = -1*self.speed
		if self.rect.x > 750:
			self.rect.x = 750
		        self.speed = -1*self.speed

	def update(self,walls,ladders,players):
		global lives
		global Gameloop
		self.rect.x += self.speed

		if collision(players,self,True):
			lives -= 3
			Gameloop = False

		ladder_list = pygame.sprite.spritecollide(self,ladders,False)
		for block in ladder_list:
			if self.rect.y < block.rect.y:
				self.rect.bottom = block.rect.top
				self.wieght = 0
				break
		block_hit_list = pygame.sprite.spritecollide(self,walls,False)
	        for block in block_hit_list:
			if self.rect.y < block.rect.y:
				self.rect.bottom = block.rect.top
				self.wieght = 0
				break
		self.check_bounds(walls)


	def shoot(self,all_sprites_list,fire_list):
		global won
		if randomize(3):
			if randomize(2):
				speed = 1+won
			else:
			 	speed = -1-won
			fire = Fireball(self.rect.x+30,self.rect.y+5,fireball,speed)
			all_sprites_list.add(fire)
			fire_list.add(fire)


def show_lives(n):
	while n < 3:
		life = Block(900-n*45,60,heart2)
		all_sprites_list.add(life)
		heart_list.add(life)
		n += 1

def get_lives(alls):
	i = 0
	while i < lives:
		life = Block(900-i*45,60,heart1)
		alls.add(life)
		i += 1

def initial(alls,princess,donkey,spawn,damsel):
	get_lives(alls)
	alls.add(donkey)
	alls.add(spawn)
	alls.add(damsel)
	princess.add(damsel)


donkey = DonkeyKong(12,110,donkey,1)
spawn = Spawn(100,560,wall)
damsel = Spawn(240,33,princess)

initial(all_sprites_list,princess_list,donkey,spawn,damsel)

while lives > 0 :

	if reset:
		create_board(wall_list,all_sprites_list,coins_list,ladder_list,ladder_hit_list)
		reset = False
	players_list = pygame.sprite.Group()
	player = Player(0,550,mario)
	all_sprites_list.add(player)
	players_list.add(player)
	show_lives(lives)

	while Gameloop:
		if score < 0:
			score = 0
		score1 = "Score : " + str(score)
		label = myfont.render(score1, 1, (255,255,255))
		count += 25
		if collision(ladder_list,player,False) and not collision(ladder_hit_list,player,False):
			player.jump()
		
		if count > (2520/won):
			donkey.shoot(all_sprites_list,fire_list)
			count = 0
			
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
			        sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_q:
					pygame.quit()
					sys.exit()
				elif event.key == K_a:
					player.move(-3)
				elif event.key == K_d:
					player.move(3)
				elif event.key == K_SPACE and (not collision(ladder_list,player,False) or collision(ladder_hit_list,player,False)):
					player.jump(-3)
				elif event.key == K_w and ladder_list:
					player.ladder(-0.07)
				elif event.key == K_s and ladder_list:
					player.ladder(1)

			if event.type == KEYUP:
				if event.key == K_a:
					player.move(0)
				elif event.key == K_d:
					player.move(0)
				elif event.key == K_SPACE:
					player.jump()
				elif event.key == K_w and ladder_list:
					player.ladder(0)
				elif event.key == K_s and ladder_list:
					player.ladder(0)

		screen.fill(black)
		screen.blit(label,(805,30))
		player.update(wall_list,ladder_list,coins_list,princess_list)
		donkey.update(wall_list,ladder_hit_list,players_list)
		for fire in fire_list:
			fire.update(wall_list,ladder_hit_list,players_list)
		spawn.update(fire_list)
		damsel.update(players_list)
		all_sprites_list.draw(screen)
		ladder_list.draw(screen)
		players_list.draw(screen)
		heart_list.draw(screen)
		clock.tick(100)
		pygame.display.update()
	Gameloop = True
pygame.quit()
sys.exit()

