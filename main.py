import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))

while True:
    screen.fill((31, 31, 31))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    pygame.display.flip()