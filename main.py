import pygame
import requests
import json
import math

pygame.init()
screen = pygame.display.set_mode((1280, 720))
font_big = pygame.font.SysFont("Consolas", 100)
clock = pygame.time.Clock()
frames = 0
players = []
food = []

x = 30
y = 50
snake_len = 10

class Snake:
    def __init__(self, x, y, dir, length):
        self.x = x
        self.y = y
        self.dir = dir
        self.length = length
        self.parts = []

    def update(self):
        mouse_pos = pygame.mouse.get_pos()

        self.parts.append((self.x, self.y))
        self.dir = math.atan2(mouse_pos[0] - self.x, mouse_pos[1] - self.y)
        self.x += 2 * math.sin(self.dir)
        self.y += 2 * math.cos(self.dir)

        if len(self.parts) > self.length:
            self.parts.pop(0)

    def draw(self, surface: pygame.Surface):
        for part in self.parts:
            pygame.draw.circle(surface, (255, 255, 255), part, 20)

    def post(self):
        requests.post(f"http://localhost:5000/modify/{ID}", json={"x": self.x, "y": self.y, "dir": self.dir, "length": self.length})

player = Snake(0, 0, 0, 10)

screen.fill((31, 31, 31))
txt_surface = font_big.render("connecting...", True, (255, 255, 255))
screen.blit(txt_surface, txt_surface.get_rect(center=(screen.get_size()[0] // 2, screen.get_size()[1] // 2)))
pygame.display.flip()
ID = int(requests.post("http://localhost:5000/register", json={"username": "kirby"}).content)

def get_users():
    request = requests.get("http://localhost:5000/users")
    return json.loads(request.content)

def get_food():
    request = requests.get("http://localhost:5000/food")
    return json.loads(request.content)

def leave(): requests.get(f"http://localhost:5000/remove/{ID}")

while True:
    screen.fill((31, 31, 31))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            leave()
            pygame.quit()
            exit()

    for index, p in enumerate(players):
        if index != ID - 1:
            pygame.draw.circle(screen, (255, 255, 255), (p["x"], p["y"]), 20)

    for index, f in enumerate(food):
        pygame.draw.circle(screen, (255, 0, 0), (f["x"], f["y"]), 10)
        if (f["x"] - player.x) * (f["x"] - player.x) + (f["y"] - player.y) * (f["y"] - player.y) < 400:
            player.length += 1
            requests.get(f"http://localhost:5000/remove_food/{index}")

    player.draw(screen)
    player.update()
    
    clock.tick(60)
    if frames & 1:
        player.post()
        players = get_users()
        food = get_food()
    frames += 1
    pygame.display.flip()