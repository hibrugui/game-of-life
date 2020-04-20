import pygame
import numpy as np
import time

# Inicialitzem els moduls de PyGame
pygame.init()

width, height = 1000, 1000

screen = pygame.display.set_mode((height, width))

bg = 25, 25, 25
# Pintem el fons de la pantalla
screen.fill(bg)

# Definim cel·les
CeldasX, CeldasY = 60, 60

# Altura de les cel·les
dimCeldaW = width / CeldasX
dimCeldaH = height / CeldasY

# Estat de les cel·les
gameState = np.zeros((CeldasX, CeldasY))

# Automates
gameState[5, 3] = 1
gameState[5, 4] = 1
gameState[5, 5] = 1

gameState[10, 22] = 1
gameState[11, 22] = 1
gameState[12, 22] = 1
gameState[13, 22] = 1
gameState[14, 22] = 1


# Bucle d'execució
while True:

    copyGameState = np.copy(gameState)

    screen.fill(bg)
    time.sleep(0.1)

    # Registrem events del mouse

    evs = pygame.event.get()

    for event in evs:
        mouseClick = pygame.mouse.get_pressed()

        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX / dimCeldaW)), int(np.floor(posY / dimCeldaH))
            copyGameState[celX, celY] = not mouseClick[2]

    for y in range(0, CeldasY):
        for x in range(0, CeldasX):
            # Calculem el número de cel·les annexes vives
            neighbor = gameState[(x - 1) % CeldasX, (y - 1) % CeldasY] + \
                       gameState[x % CeldasX, (y - 1) % CeldasY] + \
                       gameState[(x + 1) % CeldasX, (y - 1) % CeldasY] + \
                       gameState[(x - 1) % CeldasX, y % CeldasY] + \
                       gameState[(x + 1) % CeldasX, y % CeldasY] + \
                       gameState[(x - 1) % CeldasX, (y + 1) % CeldasY] + \
                       gameState[x % CeldasX, (y + 1) % CeldasY] + \
                       gameState[(x + 1) % CeldasX, (y + 1) % CeldasY]

            # Rule 1: Una cel·lula morta amb exactament 3 annexes vives es torna 1
            if gameState[x, y] == 0 and neighbor == 3:
                copyGameState[x, y] = 1
            # Rule 2: Una cel·lula viva amb mes de 3 o menys de 2 annexes es torna 0
            elif gameState[x, y] == 1 and (neighbor > 3 or neighbor < 2):
                copyGameState[x, y] = 0

            # Poligon de cada cel·la
            poly = [
                (x * dimCeldaW, y * dimCeldaH),
                ((x + 1) * dimCeldaW, y * dimCeldaH),
                ((x + 1) * dimCeldaW, (y + 1) * dimCeldaH),
                (x * dimCeldaW, (y + 1) * dimCeldaH)
            ]

            if copyGameState[x, y] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
            else:
                pygame.draw.polygon(screen, (255, 255, 255), poly, 0)

    # Actualitzem l'estat del joc

    gameState = np.copy(copyGameState)

    # Actualitzem la pantalla
    pygame.display.flip()
