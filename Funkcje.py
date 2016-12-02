import pygame, random, time

PURPLE = (255, 0, 255)
SCREENWIDTH=500
SCREENHEIGHT=600
ORANGE = (237,135,19)
RED = (255, 0, 0)
L_RED = (240,62,62)
GREEN = (20, 255, 140)
L_GREEN = (62,240,136)


def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_display(text, surf, font_size, center, color, x=0, y=0):
	largeText = pygame.font.Font('computer_pixel-7.ttf',font_size)
	TextSurf, TextRect = text_objects(text, largeText, color)
	if center: TextRect.center = ((SCREENWIDTH/2),(SCREENHEIGHT/2))
	else:
		TextRect.x = x
		TextRect.y = y
	surf.blit(TextSurf, TextRect)

def objects_hit(count, surf):
    font = pygame.font.Font('computer_pixel-7.ttf', 40)
    text = font.render("SCORE " + str(count), True, ORANGE)
    surf.blit(text, (1,1))

def read_floats(myfile, l, p):
	f = open(myfile, 'r')
	v = ['','','','','','','']
	j = 0
	for i in f.read():
		if i == ' ':
			v[j] = float(v[j])
			j += 1
		else: v[j] += i
	return v[l:p]
    
def quitgame():
    pygame.quit()
    quit()
