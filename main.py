import pygame, sys, time, random
from pygame.locals import *
pygame.init()
HEIGHT = 500
WIDTH = 800
GRAVITY = 0.0001

windowSurface = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('Hop Hop Hop')

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

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
		self.velocity[1] += GRAVITY*self.size**2
		
		#update position
		self.position[0] += self.velocity[0]
		self.position[1] += self.velocity[1]
		
		#stops jittering
		if self.velocity[0] > -0.001 and self.velocity[0] < 0.001:
			self.velocity[0] = 0
		if self.velocity[1] > -0.001 and self.velocity[1] < 0.001:
			self.velocity[1] = 0
		
		
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
		
		#screen limits and wrapping
		if self.position[1]+self.size > HEIGHT: 
			self.position[1] = HEIGHT - self.size
			self.velocity[1] = 0
		elif self.position[1] < 20:
			self.position[1] = 20
			self.velocity[1] = 0
		if self.position[0] > WIDTH:
			self.position[0] = -self.size+1
		elif self.position[0] < -self.size:
			self.position[0] = WIDTH-1
		
		
		self.draw()
	def damage(self, amount):
		if self.health-amount <= 0:
			print("Game over")
		else:
			self.health -= amount
	
	def heal(self, amount):
		self.health += amount
		if self.health > self.maxHealth:
			self.health = self.maxHealth
	
	def draw(self):
		pygame.draw.rect(windowSurface, BLUE, (self.position[0], self.position[1], self.size, self.size))
		
		pygame.draw.rect(windowSurface, BLACK, (5, 5, self.maxHealth, 15))
		pygame.draw.rect(windowSurface, RED, (5, 5, self.health, 15))
	
	
class Spike(object):
	def __init__(self, ):
		self.position = [-30, random.randint(50, HEIGHT-40)]
		if spawnOnRight:
			self.position[0] = WIDTH+40
	
	def draw(self):
		None
	def update():
		None
			


player = Player([30, HEIGHT-40], 60)

while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT or event.key == pygame.K_a:
				player.moving["left"] = True
			elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
				player.moving["right"] = True
			elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
				player.moving["down"] = True
			elif event.key == pygame.K_UP or event.key == pygame.K_w:
				player.moving["up"] = True
			elif event.key == pygame.K_SPACE:
				player.growing = True
			elif event.key == pygame.K_LSHIFT:
				player.shrinking = True
			elif event.key == pygame.K_h:
				player.damage(10)
			elif event.key == pygame.K_j:
				player.heal(10)
				
		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or event.key == pygame.K_a:
				player.moving["left"] = False
			elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
				player.moving["right"] = False
			elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
				player.moving["down"] = False
			elif event.key == pygame.K_UP or event.key == pygame.K_w:
				player.moving["up"] = False
			elif event.key == pygame.K_SPACE:
				player.growing = False
			elif event.key == pygame.K_LSHIFT:
				player.shrinking = False
	
	windowSurface.fill(WHITE)
	
	player.update()
	pygame.display.update()
	time.sleep(0.002)