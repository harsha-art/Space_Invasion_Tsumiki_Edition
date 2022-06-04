import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
	"""A class to represent a single alien in the fleet."""
	def __init__(self,ai_game):
		super().__init__()
		self.screen=ai_game.screen
		self.settings=ai_game.settings

		# Load the alien image and set its rect attribute.
		self.image=pygame.image.load("images/Mayoi.bmp")
		self.rect= self.image.get_rect()

		 # Start each new alien near the top left of the screen.
		self.rect.x= self.rect.width
		self.rect.y= self.rect.height
		# Store the alien's exact horizontal position.
		self.x=float(self.rect.x)

	def check_edge(self):
		"""Return True if alien is at edge of screen."""
		screen_rect = self.screen.get_rect()
		if self.rect.left <=0 or self.rect.right >= screen_rect.right:
			return True 
	
	def update(self):
		"""Move the alien right or left."""
		self.x += (self.settings.alien_speed * self.settings.fleet_direcion)
		self.rect.x = self.x