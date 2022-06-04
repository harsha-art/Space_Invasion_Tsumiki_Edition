import pygame 
class Buttons:
	def __init__(self,ai_game,msg):
		self.screen = ai_game.screen
		self.screen_rect = self.screen.get_rect()

		# Set the dimensions and properties of the button.
		self.font = pygame.font.SysFont("Gotham-Black.otf",640)
		self.font_colour = (30, 203, 225)
		self.button_colour = (129, 0, 255)
		self.button_width = 1000
		self.button_height = 500

		 # Build the button's rect object and center it.
		self.rect = pygame.Rect(0,0,self.button_width,self.button_height)
		self.rect.center = self.screen_rect.center
		# The button message needs to be prepped only once.
		self.display_message(msg)

	def display_message(self,msg):
		"""Turn msg into a rendered image and center text on the button."""
		self.msg_image = self.font.render(msg,True,self.font_colour,self.button_colour)
		self.msg_image_rect = self.msg_image.get_rect()
		self.msg_image_rect.center = self.rect.center

	def draw_button(self):
		# Draw blank button and then draw message.
		self.screen.fill(self.button_colour,self.rect)
		self.screen.blit(self.msg_image,self.msg_image_rect)
