import pygame, sys, time, random
from pygame.locals import *
import constant
import levels
import entity

def handleEvents():
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

pygame.init()

windowSurface = pygame.display.set_mode((constant.WIDTH, constant.HEIGHT), 0, 32)
pygame.display.set_caption('Hop Hop Hop')
player = entity.Player([500, 0], 60)


while True: #game loop
	handleEvents()
	
	windowSurface.fill(constant.WHITE)	
	levels.update(player)
	levels.draw(windowSurface)
	
	player.update()
	player.draw(windowSurface)
	
	pygame.display.update()
	time.sleep(0.002)