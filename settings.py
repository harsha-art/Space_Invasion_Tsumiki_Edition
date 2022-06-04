class Settings:
	"""A class to store all settings for Alien Invasion."""
	def __init__(self):
		self.bullet_speed=1.5
		self.bullet_colour=(60,60,60)
		self.bullet_width=3
		self.bullet_height=15
		self.screen_width=700
		self.screen_height=600
		self.bg_colour=(230,230,230)
		self.ship_speed = 1 
		self.bullets_allowed=7
		self.alien_speed = 1.0
		self.fleet_drop_speed = 10
		self.fleet_direcion = 1
		self.ship_limit = 3
		self.speed_up_factor = 1.1
		self.score_scale = 1.5

		self.initialize_dynamic_factors()
	
	def initialize_dynamic_factors(self):
		"""settings that change throughout the game."""
		self.alien_points = 50 
		self.ship_speed = 1
		self.bullet_speed = 1.5
		self.alien_speed = 1.0
		self.fleet_direcion = 1
	
	def increase_speed(self):
		"""Increase speed settings and alien point values."""
		self.ship_speed *= self.speed_up_factor
		self.bullet_speed *= self.speed_up_factor
		self.alien_speed *= self.speed_up_factor
		self.alien_points = int (self.alien_points * self.score_scale)   
