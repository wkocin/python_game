#!/usr/bin/env python
import pygame, random, time, copy
import Funkcje as fun
from Obiekty import *

class Gameloop:

	def __init__(self):

		self.opt = fun.read_floats('options.txt',0,3)
		self.carryOn = True
		self.count = 0
		self.dist = 0
		self.heli_speedy = 1
		self.heli_speedx = 2
		self.heli_freq = self.opt[1] #co ile milisekund pojawia sie helikopter	
		self.isl_freq = self.opt[2]
		self.cros_freq = 29000	 
		self.bar_freq = 5000
		self.vol_cof = self.opt[0]
		self.plane_freq = 4000
		self.SCREENWIDTH=500
		self.SCREENHEIGHT=600
		self.size = (self.SCREENWIDTH, self.SCREENHEIGHT)
		self.screen = pygame.display.set_mode(self.size)
		self.image = pygame.image.load("graphic/background2.png")
		self.GREEN = (20, 255, 140)
		self.BLUE = (100, 100, 255)
		self.PURPLE = (255, 0, 255)
		#generuje statek
		self.spaceship = Spaceship() 
		self.spaceship.rect.x = 160
		self.spaceship.rect.y = self.SCREENHEIGHT - 100
		#tworze wskazniki stanu statku
		self.cmeter = Cooldown()
		self.fmeter = Fuelmeter()
		#tworze zdarzenie
		self.gen_heli = pygame.USEREVENT + 1
		self.gen_isl = pygame.USEREVENT + 2
		self.gen_cros = pygame.USEREVENT + 3
		self.gen_bar = pygame.USEREVENT + 4
		self.gen_plane = pygame.USEREVENT + 5
		#listy obiektów
		self.all_sprites_list = pygame.sprite.Group() #self.all_sprites_list.add(spaceship) 
		self.all_heli_list = pygame.sprite.Group()
		self.bullet_list = pygame.sprite.Group()
		self.island_list = pygame.sprite.Group()
		self.cros_list = pygame.sprite.Group()
		self.barrel_list = pygame.sprite.Group()
		self.plane_list = pygame.sprite.Group()
		self.ex = None

	def events(self, event_list, keys_list):
		if self.dist == 0:
			self.all_sprites_list.add(self.spaceship)
		for event in event_list:
			if event.type==pygame.QUIT:
				self.carryOn=False
			if event.type == self.gen_heli:
				S = random.choice([0,1])
				H = Heli(S,self.heli_speedx,self.heli_speedy,random.choice([0,1]))
				H.rect.x = 0 if S else self.SCREENWIDTH
				H.rect.y = -50
				self.all_sprites_list.add(H)
				self.all_heli_list.add(H)
			if event.type == self.gen_isl:	
				Is = Island()
				self.island_list.add(Is)
			if event.type == self.gen_cros:
				C = Crossing()
				self.cros_list.add(C)
			if (event.type == self.gen_bar or (self.spaceship.frate <= 20 
			    and len(self.barrel_list) <= 2)) and self.ex is None:
				B = Barrel()
				self.barrel_list.add(B)
			if event.type == self.gen_plane:
				P = Plane()
				self.all_sprites_list.add(P)
				self.plane_list.add(P)
				
		if keys_list[pygame.K_LEFT] and self.ex is None:
			self.spaceship.moveLeft(4)
		if keys_list[pygame.K_RIGHT] and self.ex is None:
			self.spaceship.moveRight(4)
		if keys_list[pygame.K_UP] and self.ex is None:
			self.spaceship.moveForward(4)
		if keys_list[pygame.K_DOWN] and self.ex is None:
			self.spaceship.moveBackward(4)
		if keys_list[pygame.K_SPACE] and self.ex is None:
			if self.spaceship.crate <= 70:
				B = Bullet()
				B.music.set_volume(0.05*self.vol_cof)
				pygame.mixer.Sound.play(B.music)
				B.rect.x = self.spaceship.rect.x + 25.5
				B.rect.y = self.spaceship.rect.y
				self.spaceship.changeCool()
				self.all_sprites_list.add(B)
				self.bullet_list.add(B)

	def gamelogic(self):
		
		#paliwo
		if self.spaceship.frate == 0:
			self.ex = Explosion(self.spaceship.rect.x, self.spaceship.rect.y)
			self.all_sprites_list.add(self.ex)
			self.spaceship.frate = -1
			self.spaceship.kill()

		#wpadanie w sciany
		if ((self.spaceship.rect.y < 0 or self.spaceship.rect.y > self.SCREENHEIGHT) or (
		    self.spaceship.rect.x < 70-self.spaceship.rect.width/2 or self.spaceship.rect.x + self.spaceship.rect.width/2 > 			    self.SCREENWIDTH-70)) and self.ex is None:
			fun.message_display('Crush!', self.screen, 115, True, self.PURPLE)
			pygame.display.update()
			time.sleep(2)
			self.carryOn = False

		#wpadanie w wyspy
		for m in self.island_list:
			if pygame.sprite.collide_mask(m, self.spaceship):
				fun.message_display('Crush!', self.screen, 115, True, self.PURPLE)
				pygame.display.update()
				time.sleep(2)
				self.carryOn = False
			for bar in self.barrel_list:
				if pygame.sprite.collide_rect(m,bar): bar.kill()
			if m.rect.y > self.SCREENHEIGHT:
				self.island_list.remove(m)
		
		#wpadanie w mosty
		for c in self.cros_list:
			for ci in c.list:	
				if pygame.sprite.collide_mask(ci, self.spaceship):
					fun.message_display('Crush!', self.screen, 115, True, self.PURPLE)
					pygame.display.update()
					time.sleep(2)
					self.carryOn = False
			if c.lhill.rect.y > self.SCREENHEIGHT:
				self.cros_list.remove(c)

		#wpadanie w samoloty
		for s in self.plane_list:
			if pygame.sprite.collide_mask(s, self.spaceship):
				fun.message_display('Crush!', self.screen, 115, True, self.PURPLE)
				pygame.display.update()
				time.sleep(2)
				self.carryOn = False
			elif s.rect.y > self.SCREENHEIGHT:
				s.kill()

		#przesuwam Helikoptery w dol i horyzontalnie
		for h in self.all_heli_list:
			h.moveForward(self.heli_speedy)
			if h.rect.y > 0:
				h.move()
			if pygame.sprite.collide_mask(h, self.spaceship):
				fun.message_display('Crush!', self.screen, 115, True, self.PURPLE)
				pygame.display.update()
				time.sleep(2)
				self.carryOn = False
			elif h.rect.y > self.SCREENHEIGHT or h.rect.x > self.SCREENWIDTH:
				h.kill()

		# ruch kul i interakcje z obiektami
		for b in self.bullet_list:
			hit_list = pygame.sprite.spritecollide(b, self.all_heli_list, True) 
			#True == trafione zostan usuniete
			for h in hit_list: #100 pkt za helikopter
				b.kill()
				E = Explosion(h.rect.x, h.rect.y)
				self.all_sprites_list.add(E)
				E.music.set_volume(0.2*self.vol_cof)
				pygame.mixer.Sound.play(E.music)
				self.count += 100

		for b in self.bullet_list:
			hit_list = pygame.sprite.spritecollide(b, self.plane_list, True) 
			#True == trafione zostan usuniete
			for h in hit_list: #150 pkt za samolot
				b.kill()
				E = Explosion(h.rect.x, h.rect.y)
				self.all_sprites_list.add(E)
				E.music.set_volume(0.2*self.vol_cof)
				pygame.mixer.Sound.play(E.music)
				self.count += 150

		for b in self.bullet_list:
			for c in self.cros_list: #200 za most
				if pygame.sprite.collide_rect(b, c.bridge) and c.list.has(c.bridge):
					b.kill()
					c.list.remove(c.bridge)
					E = Explosion(c.bridge.rect.x, c.bridge.rect.y) 
					self.all_sprites_list.add(E)
					E.music.set_volume(0.2*self.vol_cof)
					pygame.mixer.Sound.play(E.music)
					self.count += 200

		for b in self.bullet_list:
			for bar in self.barrel_list:
				if pygame.sprite.collide_rect(b, bar):
					b.kill()
					E = Explosion(bar.rect.x, bar.rect.y)
					self.all_sprites_list.add(E)
					E.music.set_volume(0.2*self.vol_cof)
					pygame.mixer.Sound.play(E.music)
					bar.kill()
					if self.ex is None: 
						self.spaceship.frate += min(50,100-self.spaceship.frate)

		for b in self.bullet_list:		
			if b.rect.y < -10:
				b.kill()

		#self explosion
		if self.ex is not None and self.ex.index == 4:
			fun.message_display('You Run Out of Fuel!', self.screen, 45, True, self.PURPLE)
			pygame.display.update()
			time.sleep(2)
			self.carryOn = False

	def update(self):
		pygame.display.set_caption("River Raid")
		#self.screen.fill(self.BLUE)
		self.screen.blit(self.image, (0,0))
		pygame.draw.rect(self.screen, self.GREEN, [0,0, 70, self.SCREENHEIGHT])
		pygame.draw.rect(self.screen, self.GREEN, [self.SCREENWIDTH-70,0, 100, self.SCREENHEIGHT])
		#draw all the map elements
		self.island_list.update()
		self.island_list.draw(self.screen)
		self.cros_list.update()
		for c in self.cros_list:
			c.draw(self.screen)
		self.barrel_list.update()
		self.barrel_list.draw(self.screen)
		#draw all the 'moving' objects
		self.all_sprites_list.update()
		self.all_sprites_list.draw(self.screen)
		#cooldown measurement
		self.cmeter.crate = self.spaceship.crate
		self.cmeter.draw(self.screen)
		#fuel measurement 
		if self.ex is None: self.fmeter.frate = self.spaceship.frate
		self.fmeter.draw(self.screen)
		#podliczenie wyniku i zmiana trudnosci na jego podstawie
		self.dist += 1
		fun.objects_hit(self.count,self.screen)
		if self.heli_freq > 1000:
			self.heli_freq -= 0.01*self.count
		if self.heli_speedy < 5:
			self.heli_speedy += 0.0000001*self.dist
		#Refresh Screen
		pygame.display.update()

class Intro:

	def __init__(self):

		self.carryOn = True	
		self.SCREENWIDTH=500
		self.SCREENHEIGHT=600
		self.size = (self.SCREENWIDTH, self.SCREENHEIGHT)
		self.screen = pygame.display.set_mode(self.size)
		self.image = pygame.image.load("graphic/background.png")
		self.orange = (242, 136, 15)
		self.gold = (232, 229, 28)
		#self.blue = (181, 235, 235)
		self.text1 = "START"
		self.col1 = self.gold
		self.text2 = "OPTIONS"
		self.col2 = self.orange
		self.text3 = "QUIT"
		self.col3 = self.orange
		self.wsk_ind = 1 #na co ostatnio wskazywalem; 1 - start, 2 - options, 3 - quit
		self.wsk = ">>"
		self.colw = self.gold
	
	def events(self, event_list):
		for event in event_list:
			if event.type == pygame.QUIT:
					pygame.quit()
					quit()
			if event.type == pygame.KEYDOWN:
				if self.wsk_ind == 1:
					if event.key == pygame.K_UP:
						self.col1, self.col3 = self.col3, self.col1
						self.wsk_ind = 3
					if event.key == pygame.K_DOWN:
						self.col1, self.col2 = self.col2, self.col1
						self.wsk_ind = 2
				elif self.wsk_ind == 2:
					if event.key == pygame.K_UP:
						self.col2, self.col1 = self.col1, self.col2
						self.wsk_ind = 1
					if event.key == pygame.K_DOWN:
						self.col2, self.col3 = self.col3, self.col2
						self.wsk_ind = 3
				elif self.wsk_ind == 3:
					if event.key == pygame.K_UP:
						self.col3, self.col2 = self.col2, self.col3
						self.wsk_ind = 2
					if event.key == pygame.K_DOWN:
						self.col3, self.col1 = self.col1, self.col3
						self.wsk_ind = 1
				if event.key == pygame.K_RETURN:
					if self.wsk_ind == 1: self.carryOn = False
					if self.wsk_ind == 3: fun.quitgame()
					if self.wsk_ind == 2: return True
			
		
	def update(self):
		pygame.display.set_caption("River Raid")
		self.screen.blit(self.image, (0,0))
		fun.message_display(self.wsk, self.screen, 100, False, self.colw,50,50+(self.wsk_ind-1)*150)
		fun.message_display(self.text1, self.screen, 100, False, self.col1,100,50)
		fun.message_display(self.text2, self.screen, 100, False, self.col2,100,200)
		fun.message_display(self.text3, self.screen, 100, False, self.col3,100,350)
		pygame.display.update()
	
class Options():

	def __init__(self):
		
		self.c_ind = [int(i) for i in fun.read_floats('options.txt',3,6)]
		self.carryOn = False	
		self.SCREENWIDTH=500
		self.SCREENHEIGHT=600
		self.size = (self.SCREENWIDTH, self.SCREENHEIGHT)
		self.screen = pygame.display.set_mode(self.size)
		self.image = pygame.image.load("graphic/background.png")
		self.orange = (242, 136, 15)
		self.gold = (232, 229, 28)
		self.text1 = "VOLUME"
		if self.c_ind[0] == 1: self.text1op = " >low  medium  high"
		elif self.c_ind[0] == 2: self.text1op = "  low >medium  high"
		elif self.c_ind[0] == 3: self.text1op = "  low  medium >high" 
		self.col1 = self.gold
		self.text2 = "HELICOPTER FREQ."
		self.col2 = self.orange
		if self.c_ind[1] == 1: self.text2op = " >low  medium  high"
		elif self.c_ind[1] == 2: self.text2op = "  low >medium  high"
		elif self.c_ind[1] == 3: self.text2op = "  low  medium >high" 
		self.text3 = "ISLAND FREQ."
		self.col3 = self.orange
		if self.c_ind[2] == 1: self.text3op = " >low  medium  high"
		elif self.c_ind[2] == 2: self.text3op = "  low >medium  high"
		elif self.c_ind[2] == 3: self.text3op = "  low  medium >high" 
		self.text4 = "BACK"
		self.col4 = self.orange
		self.r_ind = 1 #na co ostatnio wskazywalem; 1 - o1, 2 - o2, 3 o3, 4- back; oi == textiop
		#self.c_ind = [2,2,2] #na ktorym slowie w opcjach jest > (1,2,3) 
		self.val = [[0.5,1,1.5],[4500,3000,1500],[16500, 11000, 5500]]

	def events(self, event_list):
		for event in event_list:
			if event.type == pygame.QUIT:
					pygame.quit()
					quit()
			if event.type == pygame.KEYDOWN:
				if self.r_ind == 1:
					if event.key == pygame.K_UP:
						self.col1, self.col4 = self.col4, self.col1
						self.r_ind = 4
					if event.key == pygame.K_DOWN:
						self.col1, self.col2 = self.col2, self.col1
						self.r_ind = 2
				elif self.r_ind == 2:
					if event.key == pygame.K_UP:
						self.col2, self.col1 = self.col1, self.col2
						self.r_ind = 1
					if event.key == pygame.K_DOWN:
						self.col2, self.col3 = self.col3, self.col2
						self.r_ind = 3
				elif self.r_ind == 3:
					if event.key == pygame.K_UP:
						self.col3, self.col2 = self.col2, self.col3
						self.r_ind = 2
					if event.key == pygame.K_DOWN:
						self.col3, self.col4 = self.col4, self.col3
						self.r_ind = 4
				elif self.r_ind == 4:
					if event.key == pygame.K_UP:
						self.col4, self.col3 = self.col3, self.col4
						self.r_ind = 3
					if event.key == pygame.K_DOWN:
						self.col4, self.col1 = self.col1, self.col4
						self.r_ind = 1
				if event.key == pygame.K_LEFT:
					if self.r_ind == 1 and self.c_ind[0] > 1 :
						self.c_ind[0] -= 1
						if self.c_ind[0] == 1: self.text1op = " >low  medium  high"
						else: self.text1op = "  low  >medium  high"
					if self.r_ind == 2 and self.c_ind[1] > 1 :
						self.c_ind[1] -= 1
						if self.c_ind[1] == 1: self.text2op = " >low  medium  high"
						else: self.text2op = "  low  >medium  high"
					if self.r_ind == 3 and self.c_ind[2] > 1 :
						self.c_ind[2] -= 1
						if self.c_ind[2] == 1: self.text3op = " >low  medium  high"
						else: self.text3op = "  low  >medium  high"
				if event.key == pygame.K_RIGHT:
					if self.r_ind == 1 and self.c_ind[0] < 3 :
						self.c_ind[0] += 1
						if self.c_ind[0] == 2: self.text1op = "  low >medium  high"
						else: self.text1op = "  low  medium >high"
					if self.r_ind == 2 and self.c_ind[1] < 3 :
						self.c_ind[1] += 1
						if self.c_ind[1] == 2: self.text2op = "  low >medium  high"
						else: self.text2op = "  low  medium >high"
					if self.r_ind == 3 and self.c_ind[2] < 3 :
						self.c_ind[2] += 1
						if self.c_ind[2] == 2: self.text3op = "  low >medium  high"
						else: self.text3op = "  low  medium >high"
				if event.key == pygame.K_RETURN and self.r_ind == 4:
					f = open('options.txt', 'w')
					s = str(self.val[0][self.c_ind[0]-1])+' '+str(self.val[1][self.c_ind[1]-1])+' '+str(self.val[2][self.c_ind[2]-1])+' '+str(self.c_ind[0])+' '+str(self.c_ind[1])+' '+str(self.c_ind[2])+' '+'end'
					f.write(s)
					self.carryOn = False


						
					
	def update(self):
		pygame.display.set_caption("River Raid")
		self.screen.blit(self.image, (0,0))
		fun.message_display(self.text1, self.screen, 60, False, self.col1,50,30)
		fun.message_display(self.text1op, self.screen, 50, False, self.col1,50,115)
		fun.message_display(self.text2, self.screen, 60, False, self.col2,50,190)
		fun.message_display(self.text2op, self.screen, 50, False, self.col2,50,275)
		fun.message_display(self.text3, self.screen, 60, False, self.col3,50,350)
		fun.message_display(self.text3op, self.screen, 50, False, self.col3,50,435)
		fun.message_display(self.text4, self.screen, 60, False, self.col4,50,510)
		pygame.display.update()
					



###################################################################

pygame.init()

while True:

	G = Gameloop()
	I = Intro()
	O = Options()
	previous_freq = G.heli_freq
	
	clock=pygame.time.Clock()
	
	while I.carryOn:
		O.carryOn = I.events(pygame.event.get())
		#print(O.carryOn)
		I.update()
		clock.tick(10)
		while O.carryOn:
			O.events(pygame.event.get())
			O.update()
			clock.tick(20)

		#O.carryOn = False

	I.carryOn = True

	ti = 0
	tc = 0

	pygame.time.set_timer(G.gen_heli, int(G.heli_freq))
	pygame.time.set_timer(G.gen_cros, int(G.cros_freq))
	pygame.time.set_timer(G.gen_isl, int(G.isl_freq))
	pygame.time.set_timer(G.gen_bar, int(G.bar_freq))
	pygame.time.set_timer(G.gen_plane, int(G.plane_freq))

	while G.carryOn:
		event_list = pygame.event.get()
		for e in event_list:
			if e.type == G.gen_isl:
				ti = pygame.time.get_ticks()
			if e.type == G.gen_cros:
				tc = pygame.time.get_ticks()
		if abs(ti - tc) < 3000:
			event_list = [e for e in event_list if e.type != G.gen_cros and e.type != G.gen_isl]
		if previous_freq - 500 >= G.heli_freq:
			pygame.time.set_timer(G.gen_heli, int(G.heli_freq))
			previous_freq = G.heli_freq 
		G.events(event_list,pygame.key.get_pressed())
		G.gamelogic()
		G.update()
		clock.tick(60)

	G.carryOn = True
	
fun.quitgame()










 












	
	
	
