import pygame 
from pygame.sprite import Sprite 
class Ships(Sprite):
	def __init__(self,ai_game):
		"""A class to manage the shooting ship."""
		super().__init__()
		self.screen=ai_game.screen
		self.settings=ai_game.settings
		self.screen_rect=ai_game.screen.get_rect()

		# Load the ship image and get its rect.
		self.image=pygame.image.load("images/Tsumiki.bmp")
		self.rect=self.image.get_rect()

		 # Start each new ship at the bottom center of the screen.
		self.rect.midbottom=self.screen_rect.midbottom

		# Store a decimal value for the ship's horizontal and vertical position.
		self.x=float(self.rect.x)
		self.y=float(self.rect.y)

		# Movement flags
		self.moving_right=False
		self.moving_left=False
		self.moving_up=False
		self.moving_down=False
	def Update(self):
		 """Update the ship's position based on movement flags."""
        # Update the ship's x value
		if self.moving_right and self.rect.right<self.screen_rect.right:
			self.x += self.settings.ship_speed
			self.rect.x=self.x
		if self.moving_left and self.rect.x>0:
			self.x -= self.settings.ship_speed
			self.rect.x = self.x

		# Update the ship's x value
		if self.moving_down and self.rect.bottom<self.screen_rect.bottom:
			self.y += self.settings.ship_speed
			self.rect.y = self.y
		if self.moving_up and self.rect.y>0:
			self.y -= self.settings.ship_speed
			self.rect.y = self.y

	def center_ship(self):
		 """Center the ship on the screen."""
		self.rect.midbottom = self.screen_rect.midbottom
		self.y = float(self.rect.y)
		self.x = float(self.rect.x)
	
	def blitme(self):
		"""Draw the ship at its current location."""
		self.screen.blit(self.image,self.rect)

