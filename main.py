import pygame
import requests
import time
import json

pygame.init()
screen = pygame.display.set_mode((1280, 720))
font_big = pygame.font.SysFont("Consolas", 100)
clock = pygame.time.Clock()
current_time = time.time()
players = []

x = 30
y = 50

screen.fill((31, 31, 31))
txt_surface = font_big.render("connecting...", True, (255, 255, 255))
screen.blit(txt_surface, txt_surface.get_rect(center=(screen.get_size()[0] // 2, screen.get_size()[1] // 2)))
pygame.display.flip()
ID = int(requests.post("http://localhost:5000/register", json={"username": "kirby"}).content)

def get_users():
    request = requests.get("http://localhost:5000/users")
    return json.loads(request.content)

while True:
    screen.fill((31, 31, 31))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    for p in players:
        pygame.draw.rect(screen, (255, 255, 255), (p["x"], p["y"], 20, 20))

    x, y = pygame.mouse.get_pos()
    
    clock.tick(60)
    if time.time() - current_time > 0.1:
        requests.post(f"http://localhost:5000/modify/{ID}", json={"x": x, "y": y, "dir": 100})
        players = get_users()
        current_time = time.time()
    pygame.display.flip()