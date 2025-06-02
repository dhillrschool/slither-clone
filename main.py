import pygame
import os

pygame.init()
screen = pygame.display.set_mode((1280, 720))

os.system("curl -X POST -H \"Content-Type: application/json\" -d '{\"username\": \"jerry\"}' http://localhost:5000/register")

while True:
    screen.fill((31, 31, 31))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    pygame.display.flip()