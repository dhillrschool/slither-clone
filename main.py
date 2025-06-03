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

screen.fill((31, 31, 31))
txt_surface = font_big.render("connecting...", True, (255, 255, 255))
screen.blit(txt_surface, txt_surface.get_rect(center=(screen.get_size()[0] // 2, screen.get_size()[1] // 2)))
pygame.display.flip()
requests.post("http://localhost:5000/register", json={"username": "kirby"})

def get_users():
    request = requests.get("http://localhost:5000/users")
    return json.loads(request.content)

requests.post("http://localhost:5000/modify/1", json={"user_id": 1, "x": 30, "y": 50, "dir": 100})

while True:
    screen.fill((31, 31, 31))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    for p in players:
        pygame.draw.rect(screen, (255, 255, 255), (p["x"], p["y"], 20, 20))
    
    clock.tick(60)
    if time.time() - current_time > 0.5:
        players = get_users()
        current_time = time.time()
    pygame.display.flip()