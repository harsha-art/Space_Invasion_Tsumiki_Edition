
class Game_stats:
	"""Statistics for Alien Invasion."""
	def __init__(self,ai_game):
		"""Initialize statistics."""
		self.settings = ai_game.settings
		self.reset_game()
		
		#Read the previous high score from a file 
		with open("high_score.txt",'r') as file_ob:
			self.high_score = file_ob.read()
		self.high_score = int(self.high_score)
		
		# Start game in an inactive state.
		self.game_active = False 
	def reset_game(self):
		"""Initialize statistics that can change during the game."""
		self.score = 0 
		self.level = 1 
		self.ship_limit = self.settings.ship_limit