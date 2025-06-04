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

class Snake:
    def __init__(self, x, y, dir, length):
        self.x = x
        self.y = y
        self.px = x
        self.py = y
        self.dir = dir
        self.length = length
        self.parts = []

    def __repr__(self):
        return f"snake at ({self.x}, {self.y}) facing {self.dir} length {self.length}"

    def update(self, move=True):
        mouse_pos = pygame.mouse.get_pos()
        speed = 2

        if pygame.mouse.get_pressed()[0]: speed = 4

        if (self.x - self.px) * (self.x - self.px) + (self.y - self.py) * (self.y - self.py) > 400:
            self.parts.append((self.x, self.y))
            self.px = self.x
            self.py = self.y
        
        if move:
            self.dir = math.atan2(mouse_pos[0] - self.x, mouse_pos[1] - self.y)
            self.x += speed * math.sin(self.dir)
            self.y += speed * math.cos(self.dir)

        if len(self.parts) > self.length:
            self.parts.pop(0)

    def draw(self, surface: pygame.Surface):
        pygame.draw.circle(surface, (255, 255, 255), (self.x, self.y), 20)
        for index, part in enumerate(self.parts):
            # if index > 0:
            #     pygame.draw.line(surface, (255, 255, 255), part, self.parts[index - 1], 40)
            pygame.draw.circle(surface, (255, 255, 255), part, 20)

    def post(self):
        requests.post(f"http://localhost:5000/modify/{ID}", json={"x": self.x, "y": self.y, "dir": self.dir, "length": self.length})

snakes: list[Snake] = []
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

def leave(): 
    requests.get(f"http://localhost:5000/remove/{ID}")
    snakes.pop(ID-1)

while True:
    screen.fill((31, 31, 31))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            leave()
            pygame.quit()
            exit()

    for index, p in enumerate(snakes):
        if index != ID - 1:
            snakes[index].draw(screen)
            snakes[index].update(move=False)

    for index, f in enumerate(food):
        pygame.draw.circle(screen, (255, 0, 0), (f["x"], f["y"]), 10)
        if (f["x"] - player.x) * (f["x"] - player.x) + (f["y"] - player.y) * (f["y"] - player.y) < 400:
            requests.get(f"http://localhost:5000/remove_food/{index}")
            player.length += 1
            break

    player.draw(screen)
    player.update()
    
    clock.tick(60)
    if frames & 1:
        player.post()
        players = get_users()
        if len(players) > len(snakes):
            for i in range(len(snakes), len(players)):
                p = players[i]
                snakes.append(Snake(p["x"], p["y"], p["dir"], p["length"]))
        for index, p in enumerate(players):
            snakes[index].x = p["x"]
            snakes[index].y = p["y"]
            snakes[index].dir = p["dir"]
            snakes[index].length = p["length"]
        food = get_food()
    frames += 1
    pygame.display.flip()