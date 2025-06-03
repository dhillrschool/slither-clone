import pygame
import requests

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
font_big = pygame.font.SysFont("Consolas", 100)

screen.fill((31, 31, 31))
txt_surface = font_big.render("connecting...", True, (255, 255, 255))
screen.blit(txt_surface, txt_surface.get_rect(center=(screen.get_size()[0] // 2, screen.get_size()[1] // 2)))
pygame.display.flip()
requests.post("http://localhost:5000/register", json={"username": "kirby"})

def get_users():
    request = requests.get("http://localhost:5000/users")
    return request.content

# requests.post("http://localhost:5000/modify", json={"user_id": 1, "x": 30, "y": 50, "dir": 100})

while True:
    screen.fill((31, 31, 31))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    clock.tick(60)
    pygame.display.flip()