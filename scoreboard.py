import pygame.font 
from pygame.sprite import Group
from ship import Ships 
class Scoreboard():
	"""A class to report scoring information."""
	def __init__(self, ai_game):
		self.ai_game= ai_game
		self.screen = ai_game.screen
		self.screen_rect = self.screen.get_rect()
		self.settings = ai_game.settings 
		self.stats = ai_game.stats 
		# Font settings for scoring information.
		self.text_colour = (30,30,30)
		self.font = pygame.font.SysFont("ScoreBoard_Font.ttf",48)
		
		# Prepare the initial score images.
		self.prep_score()
		self.prep_high_score()
		self.prep_level()
		self.prep_ships_lives()

	def prep_score(self):
        """Turn the score into a rendered image."""
		rounded_score = round(self.stats.score,-1)
		score_str = "{:,}".format(rounded_score)
		self.score_image = self.font.render(score_str,True,self.text_colour,self.settings.bg_colour)
		
		# Display the score at the top right of the screen.
		self.score_rect = self.score_image.get_rect()
		self.score_rect.right = self.screen_rect.right - 20 
		self.score_rect.top = 20 
	
	def show_score(self):
		"""Draw scores, level, and ships to the screen."""
		self.screen.blit(self.score_image,self.score_rect)
		self.screen.blit(self.high_score_image,self.high_score_rect)
		self.screen.blit(self.level_image,self.level_rect)
		self.ships.draw(self.screen)

	def prep_high_score(self):
		"""Turn the high score into a rendered image."""
		high_score = round(self.stats.high_score,-1)
		high_score_str = "{:,}".format(high_score)
		self.high_score_image = self.font.render(f"High Score: {high_score_str}",True,self.text_colour,self.settings.bg_colour)
		
		# Center the high score at the top of the screen.
		self.high_score_rect = self.high_score_image.get_rect()
		self.high_score_rect.centerx = self.screen_rect.centerx
		self.high_score_rect.y = self.score_rect.top

	def check_highscore(self):
		"""Check to see if there's a new high score."""
		self.stats.high_score = int(self.stats.high_score)
		if self.stats.score >self.stats.high_score:
			self.stats.high_score = self.stats.score
			self.prep_high_score()
			self.stats.high_score = str(self.stats.high_score)
			#Reads The high score from a file 
			with open("high_score.txt",'w') as file_object:
				file_object.write(self.stats.high_score)

	def prep_level(self):
		"""Turn the level into a rendered image."""
		level_str = str(self.stats.level)
		self.level_image = self.font.render(level_str,True,self.text_colour,self.settings.bg_colour)

		# Position the level below the score.
		self.level_rect = self.level_image.get_rect()
		self.level_rect.right = self.score_rect.right
		self.level_rect.top = self.score_rect.bottom + 10

	def update_level(self):
		self.stats.level += 1 
		self.prep_level()

	def prep_ships_lives(self):
		self.ships = Group()
		for ship_number in range(self.stats.ship_limit):
			ship_live = Ships(self.ai_game)
			ship_live.rect.x = 10 + ship_live.rect.width * ship_number
			ship_live.rect.y = 10 
			self.ships.add(ship_live)