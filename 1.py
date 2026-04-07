import pygame
import math

pygame.init()
screen = pygame.display.set_mode((800, 600))

# игрок
player = pygame.Rect(500, 300, 40, 40)

# NPC
npc = pygame.Rect(200, 300, 40, 40)

# стены
walls = [
    pygame.Rect(350, 200, 50, 200)
]

# настройки
VISION_DISTANCE = 500

clock = pygame.time.Clock()

running = True
while running:
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # управление игроком
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]: player.y -= 3
    if keys[pygame.K_s]: player.y += 3
    if keys[pygame.K_a]: player.x -= 3
    if keys[pygame.K_d]: player.x += 3

    # 🔹 1. проверка дистанции
    dx = player.centerx - npc.centerx
    dy = player.centery - npc.centery
    distance = math.hypot(dx, dy)

    can_see = False

    if distance < VISION_DISTANCE:

        # 🔹 2. проверка стены (line of sight)
        line = (npc.centerx, npc.centery, player.centerx, player.centery)

        blocked = False
        for wall in walls:
            if wall.clipline(line):
                blocked = True
                break

        if not blocked:
            can_see = True

    # 🔥 действие
    if can_see:
        print("NPC стреляет!")

    # --- ОТРИСОВКА ---
    pygame.draw.rect(screen, (0, 0, 255), player)  # игрок
    pygame.draw.rect(screen, (255, 0, 0), npc)     # NPC

    # стены
    for wall in walls:
        pygame.draw.rect(screen, (100, 100, 100), wall)

    # линия зрения (для дебага)
    color = (0, 255, 0) if can_see else (255, 0, 0)
    pygame.draw.line(screen, color, npc.center, player.center, 2)

    pygame.display.update()
    clock.tick(60)