import pygame, sys, time, random
from pygame.locals import *
import entity
import constant

pygame.init()

windowSurface = pygame.display.set_mode((constant.WIDTH, constant.HEIGHT), 0, 32)
pygame.display.set_caption('Hop Hop Hop')


player = entity.Player([500, 0], 60)
spikes = []
for i in range(10):
	spikes.append(entity.Spike([200+entity.Spike.width*i, constant.HEIGHT-entity.Spike.height]))
wall = entity.Wall([200, 200], 100, 100)

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
			elif event.key == pygame.K_j:
				player.heal(100)
				
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
	
	windowSurface.fill(constant.WHITE)
	
	for spike in spikes:
		spike.update(player)
		spike.draw(windowSurface)
	
	
	player.update()
	player.draw(windowSurface)
	wall.update(player)
	wall.draw(windowSurface)
	pygame.display.update()
	time.sleep(0.002)