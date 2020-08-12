# Plantilla para añadir música y efectos de sonido a un videojuego hecho con Pygame

import pygame
from pygame.locals import *
...
...
pygame.mixer.pre_init(48000, -16, 2, 512)
	# frecuencia (Tasa de muestreo de la pista mp3)
	# bits por muestra
	# stereo/mono (2/1)
	# tamaño buffer (menor = menos lag)
pygame.mixer.init()
pygame.init()
...
...
# Carga de efectos de sonido
sonidoDisparo = pygame.mixer.Sound("sfx/shoot.wav")
sonidoSelect = pygame.mixer.Sound("sfx/select.wav")
sonidoStart = pygame.mixer.Sound("sfx/start.wav")
sonidoReady = pygame.mixer.Sound("sfx/vf2/announcer/ReadyGo!.wav")
sonidoGameOver = pygame.mixer.Sound("sfx/vf2/announcer/GameOver.wav")
sonidoExcellent = pygame.mixer.Sound("sfx/vf2/announcer/Excellent.wav")
sonidoGoodJob = pygame.mixer.Sound("sfx/vf2/announcer/GoodJob.wav")
...
...
# Música
# https://www.pygame.org/docs/ref/music.html#module-pygame.mixer.music
	# Justo después de dibujar la pantalla de inicio (pygame.display.flip()) (o antes, funciona igual)
	pygame.mixer.music.load('music/Futurama-Theme_Song.mp3')
	pygame.mixer.music.play(-1)
	# -1 es para reproducción continua, hay más modos
	# Para cambiar de música simplemente hacer otro load (para la actual y carga la nueva) y play
...
...
# sfx (Special effects)
# https://www.pygame.org/docs/ref/mixer.html
	# ej.: Durante el juego
	sonidoDisparo.play()
	# En el mismo sitio que dibujas el disparo, ambas instrucciones deben estar lo más cerca posible

	# ej.: Fin de juego
	if rectanguloNave.colliderect(rectangulosInvaders[i]):
					# Derrota
					terminado = True
					pygame.mixer.music.stop()
					sonidoGameOver.play()
					pygame.time.wait(900)
	# Paramos la música
	# Reproducimos el sonido "Game Over"
	# Esperamos +- lo que dura la pista de "Game Over" +- 1"