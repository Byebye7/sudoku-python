import pygame
from settings import *

class Button:
	def __init__(self,x,y,width,height,text=None,color=(72,72,72),highlightcolor=(189,189,189),function=None,params=None):
		self.image = pygame.Surface((width,height))
		self.pos = (x,y)
		self.rect = self.image.get_rect()
		self.rect.topleft = self.pos
		self.text = text
		self.color = color
		self.highlightcolor = highlightcolor
		self.function = function
		self.params = params
		self.highlighted = False
		if self.text:
			self.textSurface = pygame.font.Font("freesansbold.ttf",20).render(text,True,BLACK)
			self.textRect = self.textSurface.get_rect()
			self.textRect.center  = (x+(width/2),y+(height/2))

	def pressed(self,mouse):
		if self.rect.collidepoint(mouse):
			return True

	def update(self,mouse):
		if self.rect.collidepoint(mouse):
			self.highlighted = True
		else:
			self.highlighted = False


	def draw(self,window):
		if self.highlighted:
			self.image.fill(self.highlightcolor)
		else:
			self.image.fill(self.color)

		window.blit(self.image,self.pos)
		if self.text:
			window.blit(self.textSurface,self.textRect)


