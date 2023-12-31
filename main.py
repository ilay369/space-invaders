import math
import random

import pygame
from pygame import mixer



pygame.init()
clock = pygame.time.Clock()

#create the screen
screen = pygame.display.set_mode((800,600))

# Background
background = pygame.image.load('static/images/background.png')

mixer.music.load("static/music/background.wav")
mixer.music.play(-1)


# Caption and Icon
pygame.display.set_caption("space invaders")
icon = pygame.image.load('static/images/ufo.png')
pygame.display.set_icon(icon)

# Player
playerimage= pygame.image.load('static/images/player.png')
playerX = 370
playerY = 480
playerX_change = 0

bulletimage= pygame.image.load('static/images/bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 5
bullet_state = "ready"

# Enemy
enemyimage = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range (num_of_enemies):
	enemyimage.append(pygame.image.load('static/images/enemy.png'))
	enemyX.append(random.randint(0,735))
	enemyY.append(random.randint(50,150))
	enemyX_change.append(2)
	enemyY_change.append(40)


score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10
# Game Over text
over_font = pygame.font.Font('freesansbold.ttf', 64)

gameover = False

def show_score(x, y):
	score = font.render("Score : "+ str(score_value), True, (255,255,255))
	screen.blit(score, [x,y])

def game_over_text():
	global gameover
	display_over_text = over_font.render("GAME OVER", True, (255,255,255))
	screen.blit(display_over_text, (200,250))
	display_restart = font.render("Press Space to Restart", True, (255,255,255))
	screen.blit(display_restart, (215,350))
	gameover = True

def player(x, y):
	screen.blit(playerimage,(x,y))

def enemy(x, y, i):
	screen.blit(enemyimage[i],(x,y))

def fire_bullet(x, y):
	global bullet_state
	bullet_state = "fire"
	screen.blit(bulletimage,(x+16,y+10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
	distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
	if distance < 27:
		return True
	else:
		return False


	
# Game Loop
running = True
while running:

	# RGB = Red, Green, Blue
	screen.fill((0, 0, 0))
	screen.blit(background,(0,0))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	
	# if keystroke is pressed check whether right or left
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				playerX_change = -5
			if event.key == pygame.K_RIGHT:
				playerX_change = 5
			if event.key == pygame.K_SPACE:
				if bullet_state == "ready":
						bullet_sound = mixer.Sound('static/music/laser.wav')
						bullet_sound.play()
						bulletX = playerX
						fire_bullet(bulletX,bulletY)
				

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				playerX_change = 0
			if event.key == pygame.K_SPACE and gameover:
				enemyX = [random.randint(0, 735) for _ in range(6)]
				enemyY = [random.randint(50, 150) for _ in range(6)]
				playerX = 370
				playerY = 480
				score_value = 0
				gameover = False
			
	
	# 5 = 5 + -0.1 -> 5 = 5 - 0.1
	# 5 = 5 + 0.1

	#checking for boundaries of spaceship so it doesn't go of out of bounds
	playerX += playerX_change

	if playerX <= 0:
		playerX = 0
	elif playerX >= 736:
		playerX = 736
	#Enemy Movement
	for i in range(num_of_enemies):
		# game over
		if enemyY[i] > 440:
			for j in range(num_of_enemies):
				enemyY[j] = 2000
			game_over_text()
			break
			
		enemyX[i] += enemyX_change[i]
		if enemyX[i] <= 0:
			enemyX_change[i] = 2
			enemyY[i] += enemyY_change[i]
		elif enemyX[i] >= 736:
			enemyX_change[i] = -2
			enemyY[i] += enemyY_change[i]

		collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
		if collision:
			explosion_sound = mixer.Sound('static/music/explosion.wav')
			explosion_sound.play()
			bulletY = 480
			bullet_state = "ready"
			score_value += 1
			enemyX[i] = random.randint(0,735)
			enemyY[i] = random.randint(50,150)



		enemy(enemyX[i],enemyY[i], i)

	if bulletY <= 0 :
		bulletY = 480
		bullet_state = "ready"

	if bullet_state == "fire":
		fire_bullet(bulletX,bulletY)
		bulletY -= bulletY_change

	
	
		

	player(playerX,playerY)
	show_score(textX, textY)
	pygame.display.update()




