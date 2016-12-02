import pygame
import random
import Funkcje as fun

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (20, 255, 140)
PURPLE = (255, 0, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 100, 255)
L_BLUE = (12, 219, 242)
BLACK = (0,0,0)

SCREENWIDTH=500
SCREENHEIGHT=600
 
class Spaceship(pygame.sprite.Sprite):

	def __init__(self):
		super().__init__()

		self.image = pygame.image.load("graphic/spaceship3.png") 
		self.rect = self.image.get_rect()
		self.mask = pygame.mask.from_surface(self.image)
		self.crate = 0
		self.frate = 100

	def moveRight(self, pixels):
		self.rect.x += pixels

	def moveLeft(self, pixels):
		self.rect.x -= pixels

	def moveForward(self, pixels):
		self.rect.y -= pixels

	def moveBackward(self, pixels):
		self.rect.y += pixels

	#cooldown rate [0,100]
	def changeCool(self):
		if self.crate <= 90:
			self.crate += 10
		else:
			self.crate = 100

	def update(self):
		if self.crate > 0.5:
			self.crate -= 0.5
		if self.frate > 0.1:
			self.frate -= 0.1
		if self.frate > 0 and self.frate <= 0.1: 
			self.frate = 0
	
        
class Heli(pygame.sprite.Sprite):
    
    #S = z lewej czy z prawej; back = czy zawraca
    def __init__(self, S, speedx, speedy, back):
        super().__init__()
        self.S = S
        if self.S == 0:
            self.image = pygame.image.load("graphic/helip.png")
            self.image = pygame.transform.scale(self.image, (91,38))
            self.mask = pygame.mask.from_surface(self.image)
        if self.S == 1:
            self.image = pygame.image.load("graphic/helil.png")
            self.image = pygame.transform.scale(self.image, (84,31))
            self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.speedx = speedx
        self.speedy = speedy
        self.back = back
    
    #uwaga: zalezne od wielkości planszy
    def move(self):
        if self.back: 
            if self.S:
                if self.rect.x > int(500/2):
                    self.image = pygame.transform.flip(self.image, True, False)
                    self.mask = pygame.mask.from_surface(self.image)
                    self.S = 1-self.S
                    self.back = 1 - self.back        
            else:
                if self.rect.x < int(500/2):
                    self.image = pygame.transform.flip(self.image, True, False)
                    self.mask = pygame.mask.from_surface(self.image)
                    self.S = 1-self.S
                    self.back = 1 - self.back             
        if self.S == 0:
            self.rect.x -= self.speedx
        if self.S == 1:
            self.rect.x += self.speedx

    def moveForward(self, speed):
        self.rect.y += self.speedy
 
    def changeSpeed(self, speed):
        self.speedy = speed

class Plane(pygame.sprite.Sprite):

	def __init__(self):
		super().__init__()

		self.SCREENHEIGHT=600
		self.SCREENWIDTH=500
		self.image = pygame.transform.flip(pygame.image.load("graphic/plane2.png"), False, True)
		#self.image = pygame.transform.scale(self.image, (84,31))
		self.mask = pygame.mask.from_surface(self.image)
		self.rect = self.image.get_rect()
		self.rect.x = random.randint(70,self.SCREENWIDTH-70-self.rect.width)
		self.rect.y = -100-self.rect.height

	def update(self):
		self.rect.y += 3
	

        
class Bullet(pygame.sprite.Sprite):

	def __init__(self):
		super().__init__()

		self.image = pygame.transform.scale(pygame.image.load("graphic/bullet.png"), (4,5))
		self.rect = self.image.get_rect()
		self.music = pygame.mixer.Sound("sound/Shot2.wav")

	def update(self):
		self.rect.y -= 5

class Explosion(pygame.sprite.Sprite):

	def __init__(self, x, y):
		super(Explosion, self).__init__()

		self.x = x
		self.y = y
		self.images = []
		for i in range(3,-1,-1):
			self.images.append(pygame.image.load('graphic/ex%i.png' % i))
		self.index = 0
		self.time = 0
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.x = self.x
		self.rect.y = self.y
		self.music = pygame.mixer.Sound("sound/Blast.wav")

	def update(self):
		self.time += 1
		if self.time % 5 == 0:
			self.index += 1
			if self.index == 4: #>= len(self.images):
				self.kill()
			else: self.image = self.images[self.index]    

#zależy od  wielkosci display
class Cooldown(pygame.sprite.Sprite):
    
	def __init__(self):
		super().__init__()

		self.SCREENHEIGHT=600
		self.rect = pygame.Rect(3,self.SCREENHEIGHT-109,24,104)
		self.letters = ["C","O","O","L"]
		self.crate = 0

	def draw(self, surf):
		pygame.draw.rect(surf, BLACK, self.rect, 2)
		if self.crate <= 70:
			pygame.draw.rect(surf, L_BLUE, pygame.Rect(5,self.SCREENHEIGHT-6-self.crate, 21, self.crate))
		else:
			pygame.draw.rect(surf, RED, pygame.Rect(5,self.SCREENHEIGHT-6-self.crate, 21, self.crate))
		for i in range(len(self.letters)):
			fun.message_display(self.letters[i], surf, 30, False, YELLOW, self.rect.x+8, self.rect.y+22*i)   

class Fuelmeter(pygame.sprite.Sprite):
    
	def __init__(self):
		super().__init__()

		self.SCREENHEIGHT=600
		self.SCREENWIDTH=500
		self.rect = pygame.Rect(self.SCREENWIDTH-26,self.SCREENHEIGHT-109,24,104)
		self.letters = ["F","U","E","L"]
		self.frate = 100

	def draw(self, surf):
		pygame.draw.rect(surf, BLACK, self.rect, 2)
		pygame.draw.rect(surf, (242,227,109), pygame.Rect(self.SCREENWIDTH-24,self.SCREENHEIGHT-6-self.frate, 21, self.frate))
		for i in range(len(self.letters)):
			fun.message_display(self.letters[i], surf, 30, False, RED, self.rect.x+8, self.rect.y+22*i)   

class Barrel(pygame.sprite.Sprite):
	
	def __init__(self):
		super().__init__()
		
		self.SCREENWIDTH=500
		self.image = pygame.transform.scale(pygame.image.load("graphic/barrel.png"),(15,20))
		self.rect = self.image.get_rect()
		self.rect.x = random.randint(75,self.SCREENWIDTH-75)

	def update(self):
		self.rect.y += 2

        
class Island(pygame.sprite.Sprite):

	def __init__(self):
		super().__init__()

		self.SCREENWIDTH=500
		self.SCREENHEIGHT=600
		self.image = pygame.image.load("graphic/island.png") 
		self.image = pygame.transform.scale(self.image, (100,200))
		self.rect = self.image.get_rect()
		self.mask = pygame.mask.from_surface(self.image)
		self.rect.x = self.SCREENWIDTH/2-self.rect.width/2
		self.rect.y = -self.rect.height - 250
	
	def update(self):
		self.rect.y += 1

class Bridge(pygame.sprite.Sprite):

	def __init__(self):
		super().__init__()

		self.image = pygame.transform.scale(pygame.image.load("graphic/most.png"), (100,100))
		self.rect = self.image.get_rect()
		self.mask = pygame.mask.from_surface(self.image)
		self.rect.x = 200
		self.rect.y = -450

	def update(self):
		self.rect.y += 1

class lHill(pygame.sprite.Sprite):

	def __init__(self):
		super().__init__()

		self.image = pygame.transform.scale(pygame.image.load("graphic/hill.png"), (201,200))
		self.rect = self.image.get_rect()
		self.mask = pygame.mask.from_surface(self.image)
		self.rect.x = 0
		self.rect.y = -500

	def update(self):
		self.rect.y += 1

class rHill(pygame.sprite.Sprite):

	def __init__(self):
		super().__init__()
		
		self.SCREENWIDTH=500
		self.image = pygame.transform.flip(pygame.transform.scale(pygame.image.load("graphic/hill.png"), (201,200)), True, False)
		self.rect = self.image.get_rect()
		self.mask = pygame.mask.from_surface(self.image)
		self.rect.x = self.SCREENWIDTH-self.rect.width
		self.rect.y = -500

	def update(self):
		self.rect.y += 1
	
class Crossing(pygame.sprite.Sprite):

	def __init__(self):
		super().__init__()

		self.bridge = Bridge()
		self.lhill = lHill() 
		self.rhill = rHill() 
		self.list = pygame.sprite.Group()
		self.list.add(self.bridge, self. lhill, self.rhill)

		
	def update(self):
		self.list.update()

	def draw(self, surf):
		self.list.draw(surf)

	
	
		
        
        
