import pygame
import constant

class Player(object):
	def __init__(self, startPosition, size):		
		self.position = startPosition
		self.velocity = [0, 0]
		self.size = size
		self.moving = {"left":False, "right":False, "up":False, "down":False}
		self.growing = False
		self.shrinking = False
		self.minSize = 5
		self.maxSize = 60
		self.sens = 0.05
		self.terminal = 5
		self.friction = 0.02
		self.maxHealth = 790
		self.health = self.maxHealth
		self.rect = pygame.Rect(self.position[0], self.position[1], self.size, self.size)

		
	def gravityAcc(self):
		return constant.GRAVITY*self.size**2
		
	def update(self):		
		if self.moving["left"]:
			self.velocity[0] -= self.sens
		if self.moving["right"]:
			self.velocity[0] += self.sens
		if self.moving["up"]:
			self.velocity[1] -= self.sens
		if self.moving["down"]:
			self.velocity[1] += self.sens
		
		#friction
		if abs(self.velocity[0]) > 0:
			self.velocity[0] -= self.friction*(abs(self.velocity[0])/self.velocity[0])
		if abs(self.velocity[1]) > 0:
			self.velocity[1] -= self.friction*(abs(self.velocity[1])/self.velocity[1])
		
		#terminal velocity
		if abs(self.velocity[0]) > self.terminal:
			self.velocity[0] = self.terminal*(abs(self.velocity[0])/self.velocity[0])
		if self.velocity[1] < -self.terminal:#no terminal vel going down
			self.velocity[1] = -self.terminal
			
		#acceleration due to gravity
		self.velocity[1] += self.gravityAcc()
		
		#update position
		self.position[0] += self.velocity[0]
		self.position[1] += self.velocity[1]
		
		
		#stops jittering
		if self.velocity[0] > -0.001 and self.velocity[0] < 0.001:
			self.velocity[0] = 0
		if self.velocity[1] > -0.001 and self.velocity[1] < 0.001:
			self.velocity[1] = 0
		
		#growing and shrinking
		if self.growing and self.size < self.maxSize:
			self.size += 0.5
			self.position[0] -= 0.25
			self.position[1] -= 0.25
			percentHealth = self.health/self.maxHealth
			self.maxHealth += 6
			self.health = self.maxHealth*percentHealth
		
		if self.shrinking and self.size > self.minSize:
			self.size -= 0.5
			self.position[0] += 0.25
			self.position[1] += 0.25
			percentHealth = self.health/self.maxHealth
			self.maxHealth -= 6
			self.health = self.maxHealth*percentHealth
		
		#screen limits
		if self.position[1]+self.size > constant.HEIGHT: 
			self.position[1] = constant.HEIGHT - self.size
			self.velocity[1] = 0
			self.moving["down"] = False
		elif self.position[1] < 20:
			self.position[1] = 20
			self.velocity[1] = 0
			self.velocity[1] = self.gravityAcc()
			self.moving["up"] = False
		
		if self.position[0]+self.size > constant.WIDTH:
			self.position[0] = constant.WIDTH-self.size
			self.velocity[0] = 0
			self.moving["right"] = False
		elif self.position[0] < 0:
			self.position[0] = 0
			self.velocity[0] = 0
			self.moving["left"] = False
		self.rect = pygame.Rect(self.position[0], self.position[1], self.size, self.size)


		
	def damage(self, amount):
		if self.health-amount <= 0:
			print("Game over")
			self.health = 0
		else:
			self.health -= amount
	
	def heal(self, amount):
		self.health += amount
		if self.health > self.maxHealth:
			self.health = self.maxHealth
			
	
	def draw(self, windowSurface):
		pygame.draw.rect(windowSurface, constant.BLUE, (self.position[0], self.position[1], self.size, self.size))
		
		pygame.draw.rect(windowSurface, constant.BLACK, (5, 5, self.maxHealth, 15))
		pygame.draw.rect(windowSurface, constant.RED, (5, 5, self.health, 15))
	
	
class Spike(object):
	width = 20
	height = 20
	
	def __init__(self, position):
		self.position = position
	
	def update(self, player):
		if player.position[0]+player.size > self.position[0] and player.position[0] < self.position[0]+self.width:
			if player.position[1]+player.size > self.position[1] and player.position[1] < self.position[1]+self.height:
				player.damage(4)
				if player.position[0]+player.size < self.position[0]+self.width/2:
					player.position[0] = self.position[0]-player.size
					player.velocity[0] = 0
				elif player.position[0] > self.position[0]+self.width/2:
					player.position[0] = self.position[0]+self.width
					player.velocity[0] = 0
				elif player.position[1]+player.size < self.position[1]+self.height/2:
					player.position[1] = self.position[1]-player.size
					player.velocity[1] = 0
	
	def draw(self, windowSurface):
		pygame.draw.polygon(windowSurface, constant.BLACK, [(self.position[0]+self.width/2, self.position[1]), (self.position[0], self.position[1]+self.height), (self.position[0]+self.width, self.position[1]+self.height)])
	
class Wall(object):
	def __init__(self, position, width, height):
		self.position = position
		self.width = width
		self.height = height
		self.rect = pygame.Rect(self.position[0], self.position[1], self.width, self.height)

	def update(self, player):
		if self.rect.colliderect(player.rect):
			if player.position[1]+player.size < self.position[1]+10:
				player.position[1] = self.position[1]-player.size
				player.velocity[1] = 0
				player.moving["down"] = False
			
			elif player.position[0] > self.position[0]+self.width-10:
				player.position[0] = self.position[0]+self.width
				player.velocity[0] = 0
				player.moving["left"] = False
			
			elif player.position[0]+player.size < self.position[0]+10:
				player.position[0] = self.position[0]-player.size
				player.velocity[0] = 0
				player.moving["right"] = False
				
			elif player.position[1] > self.position[1]+self.height-10:
				player.position[1] = self.position[1]+self.height
				player.velocity[1] = player.gravityAcc()
				player.moving["up"] = False
				

	def draw(self, windowSurface):
		pygame.draw.rect(windowSurface, constant.BLACK, (self.position[0], self.position[1], self.width, self.height))


class Box(object):
	def __init__(self, startPosition, size):
		self.position = startPosition
		self.size = size
		self.width = size
		self.height = size
		self.playerTouching = {"left":False, "right":False, "up":False, "down":False}
		
	def update(self, player):
		self.rect = pygame.Rect(self.position[0], self.position[1], self.width, self.height)
		self.playerTouching = {"left":False, "right":False, "up":False, "down":False}
		
		if self.rect.colliderect(player.rect):
			if player.position[1]+player.size < self.position[1]+5:
				self.playerTouching["down"] = True
				self.position[1] = player.position[1]+player.size
			
			elif player.position[0] > self.position[0]+self.width-5:
				self.playerTouching["left"] = True
				self.position[0] = player.position[0]-self.width
			
			elif player.position[0]+player.size < self.position[0]+5:
				self.playerTouching["right"] = True
				self.position[0] = player.position[0]+player.size
				
			elif player.position[1] > self.position[1]+self.height-5:
				self.position[1] = player.position[1]-self.height
				self.playerTouching["up"] = True


		if self.position[1]+self.size > constant.HEIGHT: 
			self.position[1] = constant.HEIGHT - self.size
			player.position[1] = self.position[1]-player.size
			player.velocity[1] = 0
			player.moving["down"] = False
		
		elif self.position[1] < 20:
			self.position[1] = 20
			player.position[1] = self.position[1]+self.height
			player.velocity[1] = 0
			player.moving["up"] = False
		
		if self.position[0]+self.size > constant.WIDTH:
			self.position[0] = constant.WIDTH-self.size
			player.position[0] = self.position[0]-player.size
			player.velocity[0] = 0
			player.moving["right"] = False
			
		elif self.position[0] < 0:
			self.position[0] = 0
			player.position[0] = self.position[0]+self.width
			player.velocity[0] = 0
			player.moving["left"] = False
			
			
		
	def draw(self, windowSurface):
		pygame.draw.rect(windowSurface, constant.GREEN, (self.position[0], self.position[1], self.size, self.size))

	
	

class Exit(object):
	width = 30
	height = 30
	
	def __init__(self, position):
		self.position = position
	
	def update(self, player):
		if player.position[1]+player.size > self.position[1] and player.position[1] < self.position[1]+self.height:
			if player.position[0] < self.position[0]+self.width and player.position[0]+player.size > self.position[0]:
				print("Level Complete")
		
	def draw(self, windowSurface):
		pygame.draw.rect(windowSurface, constant.LIGHT_GREY, (self.position[0], self.position[1], self.width, self.height))
