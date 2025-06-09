import pygame
import requests
import json
import math
import socket
from urllib.request import urlopen

pygame.init()
screen = pygame.display.set_mode((1280, 720))
font = pygame.font.SysFont("Inter", 30, True)
font_big = pygame.font.SysFont("Inter", 100, True)
clock = pygame.time.Clock()
frames = 0
players = []
user_ids = []
old_user_ids = []
food = []

class Button:
    def __init__(self, x, y, w, h, txt):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.txt = txt
        self.txt_surface = font.render(txt, True, (31, 31, 31))
        self.outline_width = 0
    
    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, (0, 127, 0), (self.x, self.y, self.w, self.h), border_radius=20)
        pygame.draw.rect(surface, (0, 255, 0), (self.x, self.y, self.w, self.h), width=int(self.outline_width), border_radius=20)
        surface.blit(self.txt_surface, self.txt_surface.get_rect(center=(self.x+0.5*self.w, self.y+0.5*self.h)))

        if pygame.Rect(self.x, self.y, self.w, self.h).collidepoint(pygame.mouse.get_pos()):
            self.outline_width += 0.125 * (5 - self.outline_width)
            if pygame.mouse.get_pressed()[0]:
                self.on_click(self.txt)
        else:
            self.outline_width -= 0.125 * self.outline_width

def get_local_ip():
    try:
        sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sk.connect(('8.8.8.8', 80))
        res = sk.getsockname()
    finally:
        sk.close()
    return res

print(get_local_ip())

def scan_servers():
    res = []

    for i in range(1, 256):
        try:
            urlopen(f"http://127.0.0.{i}:5000/food", timeout=0.005)
            res.append(i)
        except: pass

    return res

txt_surface = font_big.render("loading...", True, (255, 255, 255))
screen.blit(txt_surface, txt_surface.get_rect(center=(screen.get_size()[0] // 2, screen.get_size()[1] // 2)))
pygame.display.flip()

menu = True
available_servers = scan_servers()
selected_server = 0
buttons: list[Button] = []

def on_click(txt):
    global menu, selected_server
    menu = False
    selected_server = int(txt)


for index, id in enumerate(available_servers):
    b = Button(30 + index * 130, 30, 100, 100, str(id))
    b.on_click = on_click
    buttons.append(b)

while menu:
    screen.fill((31, 31, 31))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    for button in buttons:
        button.draw(screen)

    pygame.display.flip()
    clock.tick(60)


api = f"http://127.0.0.{selected_server}:5000"

class Snake:
    def __init__(self, x, y, dir, length, name, id=0):
        self.x = x
        self.y = y
        self.px = x
        self.py = y
        self.dir = dir
        self.name = name
        self.length = length
        self.user_id = id
        self.parts = []

    def __repr__(self):
        return f"{self.name} (#{self.user_id}) at ({self.x}, {self.y}) facing {self.dir} length {self.length}"

    def update(self, move=True):
        mouse_pos = pygame.mouse.get_pos()
        speed = 2

        if pygame.mouse.get_pressed()[0] and self.length > 10: 
            speed = 4
            self.length -= 0.1

        if (self.x - self.px) * (self.x - self.px) + (self.y - self.py) * (self.y - self.py) > 225:
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
        requests.post(f"{api}/modify/{ID}", json={"x": self.x, "y": self.y, "dir": self.dir, "length": self.length})

snakes: list[Snake] = []
player = Snake(0, 0, 0, 10, "kirby")

screen.fill((31, 31, 31))
txt_surface = font_big.render("connecting...", True, (255, 255, 255))
screen.blit(txt_surface, txt_surface.get_rect(center=(screen.get_size()[0] // 2, screen.get_size()[1] // 2)))
pygame.display.flip()
ID = int(requests.post(f"{api}/register", json={"username": "kirby"}).content)

def get_users():
    request = requests.get(f"{api}/users")
    return json.loads(request.content)

def get_food():
    request = requests.get(f"{api}/food")
    return json.loads(request.content)

def leave(): requests.get(f"{api}/remove/{ID}")

while True:
    screen.fill((31, 31, 31))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            leave()
            pygame.quit()
            exit()

    for p in snakes:
        if p.user_id != ID:
            p.draw(screen)
            p.update(move=False)

            for part in p.parts:
                if (part[0] - player.x) * (part[0] - player.x) + (part[1] - player.y) * (part[1] - player.y) < 400:
                    leave()
                    pygame.quit()
                    exit()

    for index, f in enumerate(food):
        pygame.draw.circle(screen, (255, 0, 0), (f["x"], f["y"]), 10)
        if (f["x"] - player.x) * (f["x"] - player.x) + (f["y"] - player.y) * (f["y"] - player.y) < 400:
            requests.get(f"{api}/remove_food/{index}")
            player.length += 1

    player.draw(screen)
    player.update()
    
    clock.tick(60)
    if frames & 1:
        player.post()
        user_ids = []
        old_user_ids = []

        for p in players:
            old_user_ids.append(p["user_id"])
        
        players = get_users()

        for p in players:
            user_ids.append(p["user_id"])
        
        if len(players) > len(snakes):
            for i in range(len(snakes), len(players)):
                p = players[i]
                snakes.append(Snake(p["x"], p["y"], p["dir"], p["length"], p["username"], id=int(p["user_id"])))
        
        if len(players) < len(snakes):
            snakes = [snake for snake in snakes if snake.user_id in user_ids]
        
        for index, snake in enumerate(snakes):
            p = players[user_ids.index(snake.user_id)]
            snake.x = p["x"]
            snake.y = p["y"]
            snake.dir = p["dir"]
            snake.length = p["length"]
        food = get_food()
    frames += 1
    pygame.display.flip()