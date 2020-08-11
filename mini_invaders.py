#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Mini-invaders, version 0.14
# +5 invaders al destruir la nave nodriza (van más rápido), arreglado bug nodriza
# Modo pantalla completa (cutre)
# Evolución de la intro a PyGame de Nacho Cabanes por Alberto Ferreiro

import pygame
from pygame.locals import *
import random
pygame.mixer.pre_init(48000, -16, 2, 512)
	# frecuencia (Tasa de muestreo de la pista mp3)
	# bits por muestra
	# stereo/mono (2/1)
	# tamaño buffer (menor = menos lag)
pygame.mixer.init()
pygame.init()

ancho = 800
alto = 600
fullscreen = False

pantalla = pygame.display.set_mode((ancho, alto))
pygame.key.set_repeat(1,25)		# Retraso inicial, retrasos consecutivos
reloj = pygame.time.Clock()
pygame.mouse.set_visible(False)



# Carga de imágenes
imagenFondo = pygame.image.load("sprites/background.png")
rectanguloFondo = imagenFondo.get_rect()
imagenNave = pygame.image.load("sprites/x_wing.png")
rectanguloNave = imagenNave.get_rect()
imagenUfo = pygame.image.load("sprites/ufo.png")
rectanguloUfo = imagenUfo.get_rect()
imagenInvader = pygame.image.load("sprites/spaceinvader.png")
rectangulosInvaders = {}
invadersActivos = {}
velocidadesX = {}
velocidadesY = {}
imagenDisparo = pygame.image.load("sprites/disparo.png")
rectanguloDisparo = imagenDisparo.get_rect()
imagenPresentacion = pygame.image.load("sprites/background_planet_express.png")
rectanguloPresentacion = imagenPresentacion.get_rect()

# Carga de fuentes de texto
letra30 = pygame.font.SysFont("Arial", 30)
imagenTextoPresentacion = letra30.render('Pulsa intro para jugar', True, (255,255,255))
rectanguloTextoPresentacion = imagenTextoPresentacion.get_rect()
rectanguloTextoPresentacion.centerx = pantalla.get_rect().centerx
rectanguloTextoPresentacion.centery = 560

letra18 = pygame.font.SysFont("Arial", 18)

# Carga de música y efectos de sonido
sonidoDisparo = pygame.mixer.Sound("sfx/shoot.wav")
sonidoSelect = pygame.mixer.Sound("sfx/select.wav")
sonidoStart = pygame.mixer.Sound("sfx/start.wav")
sonidoReady = pygame.mixer.Sound("sfx/ReadyGo!.wav")
sonidoGameOver = pygame.mixer.Sound("sfx/GameOver.wav")
sonidoExcellent = pygame.mixer.Sound("sfx/Excellent.wav")
sonidoGoodJob = pygame.mixer.Sound("sfx/GoodJob.wav")

partidaEnMarcha = True

while partidaEnMarcha:
	# ---- Presentacion ---- #
	pantalla.fill((0,0,0))
	pantalla.blit(imagenPresentacion, rectanguloPresentacion)
	pantalla.blit(imagenTextoPresentacion, rectanguloTextoPresentacion)
	pygame.display.flip()
	pygame.mixer.music.load('music/Futurama-Theme_Song.mp3')
	pygame.mixer.music.play(-1)

	linkStart = False
	while not linkStart:
		pygame.time.wait(100)
		for event in pygame.event.get():
			keys = pygame.key.get_pressed()
			if keys[pygame.K_RETURN]:
				sonidoReady.play()
				pygame.mixer.music.fadeout(900)
				pygame.time.wait(900)
				linkStart = True
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
			# Swich entre ventana y pantalla completa
			if keys[pygame.K_F12] and not fullscreen:
				pygame.display.set_mode((ancho, alto), pygame.FULLSCREEN)
				fullscreen = True
				pantalla.blit(imagenPresentacion, rectanguloPresentacion)
				pantalla.blit(imagenTextoPresentacion, rectanguloTextoPresentacion)
				pygame.display.flip()
			elif keys[pygame.K_F12] and fullscreen:
				pygame.display.set_mode((ancho, alto))
				fullscreen = False
				pantalla.blit(imagenPresentacion, rectanguloPresentacion)
				pantalla.blit(imagenTextoPresentacion, rectanguloTextoPresentacion)
				pygame.display.flip()


	# ---- Nueva partida ---- #
	puntos = 0
	cantidadInvaders = 10
	velocidadInvaders = 4
	rectanguloNave.left = ancho/2
	rectanguloNave.top = alto-70
	rectanguloUfo.top = 20
	pygame.mixer.music.load('music/Ride_The_Tiger_SEGA_Genesis.mp3')
	pygame.mixer.music.play(-1)

	# Se generan los invaders
	for i in range(0, cantidadInvaders+1):
		rectangulosInvaders[i] = imagenInvader.get_rect()
		rectangulosInvaders[i].left = random.randrange(50, 750)
		rectangulosInvaders[i].top = random.randrange(10,300)
		invadersActivos[i] = True
		velocidadesX[i] = velocidadInvaders
		velocidadesY[i] = velocidadInvaders

	disparoActivo = False
	ufoActivo = True
	terminado = False

	while not terminado:
		# ---- Comprobar acciones del usuario ---- #
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				terminado = True
				partidaEnMarcha = False
		keys = pygame.key.get_pressed()
		if keys[K_LEFT] and rectanguloNave.left > 0:
			rectanguloNave.left -= 8
		if keys[K_RIGHT] and rectanguloNave.left < ancho-60:
			rectanguloNave.left += 8
		if keys[K_SPACE] and not disparoActivo:
			disparoActivo = True
			rectanguloDisparo.left = rectanguloNave.left + 27
			rectanguloDisparo.top = rectanguloNave.top - 12
			sonidoDisparo.play()

		# ---- Actualizar estado ---- #
		for i in range(0, cantidadInvaders+1):
			rectangulosInvaders[i].left += velocidadesX[i]
			rectangulosInvaders[i].top += velocidadesY[i]
			if rectangulosInvaders[i].left < 0 or rectangulosInvaders[i].right > ancho:
				velocidadesX[i] = -velocidadesX[i]
			# El -40 evita que los Invaders salgan de la pantalla por debajo
			if rectangulosInvaders[i].top < 0 or rectangulosInvaders[i].top > alto-40:
				velocidadesY[i] = -velocidadesY[i]

		if ufoActivo != False:
			rectanguloUfo.left += 8
			if rectanguloUfo.right > ancho:
				rectanguloUfo.left = 0
		else:
			rectanguloUfo.left = ancho

		if disparoActivo:
			rectanguloDisparo.top -= 32
			if rectanguloDisparo.top <= 0:
				disparoActivo = False

		# ---- Comprobar colisiones ---- #
		for i in range(0, cantidadInvaders+1):
			if invadersActivos[i]:
				if rectanguloNave.colliderect(rectangulosInvaders[i]):
					# Derrota
					terminado = True
					pygame.mixer.music.stop()
					sonidoGameOver.play()
					pygame.time.wait(900)
				if disparoActivo:
					if rectanguloDisparo.colliderect(rectangulosInvaders[i]):
						invadersActivos[i] = False
						disparoActivo = False
						puntos += 10

		cantidadInvadersActivos = 0
		for i in range(0, cantidadInvaders+1):
			if invadersActivos[i]:
				cantidadInvadersActivos = cantidadInvadersActivos + 1

		if disparoActivo:
			if rectanguloDisparo.colliderect(rectanguloUfo):
				if cantidadInvadersActivos != 0:
					sonidoGoodJob.play()
				ufoActivo = False
				disparoActivo = False
				puntos += 50
				cantidadInvaders += 5
				cantidadInvadersActivos += 5
				velocidadInvaders += 2
				for i in range(cantidadInvaders+1-5, cantidadInvaders+1+5):
					rectangulosInvaders[i] = imagenInvader.get_rect()
					rectangulosInvaders[i].left = random.randrange(50, 750)
					rectangulosInvaders[i].top = random.randrange(10,300)
					invadersActivos[i] = True
					velocidadesX[i] = velocidadInvaders
					velocidadesY[i] = velocidadInvaders

		# Victoria
		if not ufoActivo and cantidadInvadersActivos == 0:
			terminado = True
			pygame.mixer.music.stop()
			sonidoExcellent.play()
			pygame.time.wait(900)

		# ---- Dibujar elementos en pantalla ---- #
		pantalla.fill((0,0,0))
		pantalla.blit(imagenFondo, rectanguloFondo)
		for i in range(0, cantidadInvaders+1):
			if invadersActivos[i]:
				pantalla.blit(imagenInvader, rectangulosInvaders[i])
		if ufoActivo:
			pantalla.blit(imagenUfo, rectanguloUfo)
		if disparoActivo:
			pantalla.blit(imagenDisparo, rectanguloDisparo)
		pantalla.blit(imagenNave, rectanguloNave)

		imagenPuntuacion = letra18.render('Puntos ' +str(puntos), True, (155,155,0), (0,0,0))
		rectanguloPuntuacion = imagenPuntuacion.get_rect()
		rectanguloPuntuacion.left = 10
		rectanguloPuntuacion.top = 10
		pantalla.blit(imagenPuntuacion, rectanguloPuntuacion)

		pygame.display.flip()

		# ---- Control de fps ---- #
		reloj.tick(60)

# ---- Final de la partida ---- #
pygame.quit()
exit()