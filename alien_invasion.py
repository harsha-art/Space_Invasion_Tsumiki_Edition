import sys
import pygame 
from settings import Settings
from ship import Ships 
from bullet import Bullet
from alien import Alien
from time import sleep
from game_stats import Game_stats
from button import Buttons 
from scoreboard import Scoreboard

class Alien_invasion():
	"""The Main to manage game assets and behavior."""
	def __init__(self):
		pygame.init()
		self.settings=Settings()
		self.screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
		self.stats = Game_stats(self)
		self.bullets=pygame.sprite.Group()
		self.settings.screen_height=self.screen.get_height()
		self.settings.screen_width=self.screen.get_width()
		self.Ships=Ships(self)
		self.aliens=pygame.sprite.Group()
		self._create_fleet()
		self.play_button = Buttons(self,"Play")
		self.score_board = Scoreboard(self)
		pygame.display.set_caption("Alien game")
	
	def run_game(self):
		"""Runs the main loop for the game."""
		while True:
			self._check_events()
			if self.stats.game_active:
				self.Ships.Update()
				self.update_bullets()
				self._update_aliens()
			self._update_game()

	def _check_events(self):
		"""Respond to Keyboard inputs and mouse clicks."""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				self._check_keydown(event)
			elif event.type == pygame.KEYUP:
				self._check_keyup(event)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				self._check_play(mouse_pos)

	def _check_play(self,mouse_pos):
		"""Start a new game when the player clicks Play."""
		button_clicked =self.play_button.rect.collidepoint(mouse_pos)
		if button_clicked and not self.stats.game_active:
			# Reset the game settings.
			self.settings.initialize_dynamic_factors()
			self.stats.reset_game()

			# Hide the mouse cursor.
			pygame.mouse.set_visible(False)

			# Reset the game statistics.
			self.stats.game_active = True
			self.aliens.empty()
			self.bullets.empty()
			 # Create a new fleet and center the ship.
			self._create_fleet()
			self.Ships.center_ship()

			#Intialize Score
			self.score_board.prep_score()
	def _check_keydown(self,event):
		"""Respond to keypresses."""
		if event.key == pygame.K_RIGHT:
			self.Ships.moving_right = True
		elif event.key == pygame.K_LEFT:
			self.Ships.moving_left = True
		elif event.key== pygame.K_UP:
			self.Ships.moving_up = True
		elif event.key == pygame.K_DOWN:
			self.Ships.moving_down = True
		elif event.key == pygame.K_q:
			sys.exit()
		elif event.key == pygame.K_SPACE:
				self._fire_bullets()
	def _check_keyup(self,event):
		"""Respond to key releases."""
		if event.key == pygame.K_RIGHT:
			self.Ships.moving_right= False
		elif event.key == pygame.K_UP:
			self.Ships.moving_up= False
		elif event.key == pygame.K_DOWN:
			self.Ships.moving_down= False
		elif event.key == pygame.K_LEFT:
			self.Ships.moving_left= False


	def _create_fleet(self):
		 """Create the fleet of aliens."""
        # Create an alien and find the number of aliens in a row.
        # Spacing between each alien is equal to one alien width.
		alien=Alien(self)
		alien_width,alien_height=alien.rect.size
		# Determine the number of rows of aliens that fit on the screen.
		ship_height=self.Ships.rect.height
		available_space_x = self.settings.screen_width -(2 * alien_width)
		no_of_aliens = (available_space_x) // (2 * alien_width)
		 # Create the full fleet of aliens.
		available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
		no_of_rows = available_space_y // (2 * alien_height)
		for row in range(0,no_of_rows):
			for alien_number in range(0,no_of_aliens):
				self._create_alien(alien_number,row)
	def _fire_bullets(self):
		"""Create a new bullet and add it to the bullets group."""
		if len(self.bullets)< self.settings.bullets_allowed:
			new_bullet=Bullet(self)
			self.bullets.add(new_bullet)
	def update_bullets(self):
		"""Update position of the bullets and get rid of old bullets."""
        # Update bullet positions.
		self.bullets.update()
		# Get rid of bullets that have disappeared.
		for bullet in self.bullets.copy():
				if bullet.rect.bottom<=0:
					self.bullets.remove(bullet)
	def check_collisions(self):
		 """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
		collisions = pygame.sprite.groupcollide(self.bullets,self.aliens,True,True) 
		if collisions:
			for aliens in collisions.values():
				self.stats.score += self.settings.alien_points * len(aliens)
			self.score_board.prep_score()
			self.score_board.check_highscore()
		if not self.aliens:
			self.bullets.empty()
			self._create_fleet()
			self.settings.increase_speed()
			self.score_board.update_level()
			self.score_board.prep_ships_lives()
	def _create_alien(self,alien_number,row):
		"""Create an alien and place it in the row."""
		alien=Alien(self)
		alien_width,alien_height=alien.rect.size
		alien.x=alien_width + 2 * alien_width * alien_number
		alien.rect.x=alien.x
		alien.rect.y= alien.rect.y + (2* alien_height)* row 
		self.aliens.add(alien)
		self.check_collisions()
	
	def _update_aliens(self):
		"""
        Check if the fleet is at an edge,
         then update the positions of all aliens in the fleet.
        """
		self._check_fleet_edges()
		self.aliens.update()
		 # Look for alien-ship collisions.
		if pygame.sprite.spritecollideany(self.Ships,self.aliens):
			self.ship_hit()
		self._check_aliens_bottom()

	def _check_aliens_bottom(self):
		 """Check if any aliens have reached the bottom of the screen."""
		screen_rect = self.screen.get_rect()
		for alien in self.aliens.sprites():
			if alien.rect.bottom >= screen_rect.bottom:
				 # Treat this the same as if the ship got hit.
				self.ship_hit()
				break
	
	def ship_hit(self):
		 """Respond to the ship being hit by an alien."""
		if self.stats.ship_limit > 0:
			 # Decrement ships_left
			self.stats.ship_limit -= 1 
			# Destroy any remaining aliens and bullets.
			self.aliens.empty()
			self.bullets.empty()

			# Create a new fleet and center the ship.
			self._create_fleet()
			self.Ships.center_ship()

			#update scoreboard.
			self.score_board.prep_ships_lives()
		else:
			self.stats.game_active = False
			pygame.mouse.set_visible(True)
		#Pause 
		sleep(0.25)

	def _check_fleet_edges(self):
		"""Respond appropriately if any aliens have reached an edge."""
		for alien in self.aliens.sprites():
			if alien.check_edge():
				self.change_fleet_direction()
				break
	
	def change_fleet_direction(self):
		"""Drop the entire fleet and change the fleet's direction."""
		for alien in self.aliens.sprites():
			alien.rect.y += self.settings.fleet_drop_speed
		self.settings.fleet_direcion  *= -1
	
	def _update_game(self):
		"""Update images on the screen, and flip to the new screen."""
		self.screen.fill(self.settings.bg_colour)
		self.Ships.blitme()
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()
		self.aliens.draw(self.screen)
		self.score_board.show_score()
		if not self.stats.game_active:
			self.play_button.draw_button()
		pygame.display.flip()

if __name__=="__main__":
	# Make a game instance, and run the game.
	ai=Alien_invasion()
	ai.run_game()