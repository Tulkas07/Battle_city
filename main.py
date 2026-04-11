import pygame
import math as m
from pygame import *
import random

pygame.init()

img_player = "player_tank_sprite.png"
img_enemy = "enemy_tank_sprite.png"
img_wall = "wall_sprite.png"
img_bullet = "bullet.png"

class GSprite(sprite.Sprite):
    def __init__(self, entity_img, entity_pos_x, entity_pos_y, entity_size, entity_speed):
        super().__init__()
        self.image = transform.scale(image.load(entity_img), (entity_size, entity_size))
        self.rect = self.image.get_rect()
        self.speed = entity_speed
        self.rect.x = entity_pos_x
        self.rect.y = entity_pos_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        

class Player(GSprite):
    def __init__(self, entity_img, entity_pos_x, entity_pos_y, entity_size,  entity_speed):
        super().__init__(entity_img, entity_pos_x, entity_pos_y, entity_size, entity_speed)
        self.direction = "UP"
        self.last_shot_time = 0
        self.shoot_cooldown = 1250

    
    def movement(self):
        self.old_x = self.rect.x
        self.old_y = self.rect.y

        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.rect.x -= self.speed
            if self.direction != "LEFT" and self.direction == "UP":
                self.direction = "LEFT"
                self.image = pygame.transform.rotate(self.image, 90)
            elif self.direction != "LEFT" and self.direction == "RIGHT":
                self.direction = "LEFT"
                self.image = pygame.transform.rotate(self.image, 180)
            elif self.direction != "LEFT" and self.direction == "DOWN":
                self.direction = "LEFT"
                self.image = pygame.transform.rotate(self.image, 270)

        if keys[K_RIGHT]:
            self.rect.x += self.speed
            if self.direction != "RIGHT" and self.direction == "UP":
                self.direction = "RIGHT"
                self.image = pygame.transform.rotate(self.image, 270)
            elif self.direction != "RIGHT" and self.direction == "LEFT":
                self.direction = "RIGHT"
                self.image = pygame.transform.rotate(self.image, 180)
            elif self.direction != "RIGHT" and self.direction == "DOWN":
                self.direction = "RIGHT"
                self.image = pygame.transform.rotate(self.image, 90)
            
        if keys[K_DOWN]:
            self.rect.y += self.speed
            if self.direction != "DOWN" and self.direction == "UP":
                self.direction = "DOWN"
                self.image = pygame.transform.rotate(self.image, 180)
            elif self.direction != "DOWN" and self.direction == "RIGHT":
                self.direction = "DOWN"
                self.image = pygame.transform.rotate(self.image, 270)
            elif self.direction != "DOWN" and self.direction == "LEFT":
                self.direction = "DOWN"
                self.image = pygame.transform.rotate(self.image, 90)
                
        if keys[K_UP]:
            self.rect.y -= self.speed
            if self.direction == "RIGHT" and self.direction != "UP":
                self.direction = "UP"
                self.image = pygame.transform.rotate(self.image, 90)
            elif self.direction == "LEFT" and self.direction != "UP":
                self.direction = "UP"
                self.image = pygame.transform.rotate(self.image, 270)
            elif self.direction == "DOWN" and self.direction != "UP":
                self.image = pygame.transform.rotate(self.image, 180)
                self.direction = "UP"
                
    def collision(self, walls):
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                     
                if self.direction == "LEFT":
                    self.rect.x += 0
                elif self.direction == "RIGHT":
                    self.rect.x -= 0
                
                elif self.direction == "UP":
                    self.rect.y += 0
                elif self.direction == "DOWN":
                    self.rect.y -= 0

    def shoot(self):
        keys = pygame.key.get_pressed()
        timer = pygame.time.get_ticks()

        if keys[K_f] and timer - self.last_shot_time > self.shoot_cooldown:
            bullet = PlayerBullet(img_bullet, self.rect.centerx, self.rect.centery, 15, 5, self.direction)
            player_bullet_group.add(bullet)

            self.last_shot_time = timer   



class PlayerBullet(GSprite):
    def __init__(self, entity_img, entity_pos_x, entity_pos_y, entity_size,  entity_speed, direction):
        super().__init__(entity_img, entity_pos_x, entity_pos_y, entity_size, entity_speed)
        self.direction = direction
        self.kill_count = 0
        
        if self.direction == "UP":
            self.image = pygame.transform.rotate(self.image, 90)
        elif self.direction == "DOWN":
            self.image = pygame.transform.rotate(self.image, 270)
        elif self.direction == "LEFT":
            self.image = pygame.transform.rotate(self.image, 180)
        

        self.rect = self.image.get_rect(center=(entity_pos_x, entity_pos_y))

    def update(self):
        if self.direction == "UP":
            self.rect.y -= self.speed
        elif self.direction == "DOWN":
            self.rect.y += self.speed
        elif self.direction == "LEFT":
            self.rect.x -= self.speed
        elif self.direction == "RIGHT":
            self.rect.x += self.speed

        if pygame.sprite.spritecollide(self, walls, False):
            self.kill()

        hit_enemies = pygame.sprite.spritecollide(self, enemys_group, True)
        if hit_enemies:
            global kill_count
            kill_count += len(hit_enemies)
            self.kill()


class EnemyBullet(GSprite):
    def __init__(self, entity_img, entity_pos_x, entity_pos_y, entity_size,  entity_speed, direction):
        super().__init__(entity_img, entity_pos_x, entity_pos_y, entity_size, entity_speed)
        self.direction = direction
        
        if self.direction == "UP":
            self.image = pygame.transform.rotate(self.image, 90)
        elif self.direction == "DOWN":
            self.image = pygame.transform.rotate(self.image, 270)
        elif self.direction == "LEFT":
            self.image = pygame.transform.rotate(self.image, 180)
        

        self.rect = self.image.get_rect(center=(entity_pos_x, entity_pos_y))
    def update(self):
        if self.direction == "UP":
            self.rect.y -= self.speed
        elif self.direction == "DOWN":
            self.rect.y += self.speed
        elif self.direction == "LEFT":
            self.rect.x -= self.speed
        elif self.direction == "RIGHT":
            self.rect.x += self.speed

        if pygame.sprite.spritecollide(self, walls, False):
            self.kill()

        hit_player = pygame.sprite.spritecollide(self, player_group, True)
        if hit_player:
            global game_over
            game_over = True
            self.kill()
                    


class Enemy(GSprite):
    def __init__(self, entity_img, entity_pos_x, entity_pos_y, entity_size,  entity_speed):
        super().__init__(entity_img, entity_pos_x, entity_pos_y, entity_size, entity_speed)
        self.direction = "UP"
        self.detected = False       

    def update(self):
        if self.direction == "UP":
            self.rect.y -= self.speed
            if pygame.sprite.spritecollide(self, walls, False):
                self.image = pygame.transform.rotate(self.image, 90)
                self.direction = "LEFT"
        if self.direction == "DOWN":
            self.rect.y += self.speed
            if pygame.sprite.spritecollide(self, walls, False):
                self.image = pygame.transform.rotate(self.image, 90)
                self.direction = "RIGHT"
        if self.direction == "RIGHT":
            self.rect.x += self.speed
            if pygame.sprite.spritecollide(self, walls, False):
                self.image = pygame.transform.rotate(self.image, 90)
                self.direction = "UP"
        if self.direction == "LEFT":
            self.rect.x -= self.speed
            if pygame.sprite.spritecollide(self, walls, False):
                self.image = pygame.transform.rotate(self.image, 90)
                self.direction = "DOWN"

    def shoot(self):
        if self.detected == True and random.random() < 0.01:

            bullet = EnemyBullet(img_bullet, self.rect.centerx, self.rect.centery, 15, 5, self.direction)
            enemys_bullet_group.add(bullet)


def draw_text(text, size, color, x, y):
    font.init()
    font_style = font.Font(None, size)
    text_surface = font_style.render(text, True, color)
    rect = text_surface.get_rect(center=(x, y))
    window.blit(text_surface, rect)



window = display.set_mode((800, 600))
display.set_caption("Круті танчики")
background = transform.scale(image.load("background.png"), (800, 600))
tank_player = Player(img_player, 200, 350, 45, 3)
player_group = pygame.sprite.GroupSingle(tank_player)
tank_enemy1 = Enemy(img_enemy, 150, 250, 45, 2)
tank_enemy2 = Enemy(img_enemy, 50, 500, 45, 2)
tank_enemy3 = Enemy(img_enemy, 650, 300, 45, 2)
enemys_group = sprite.Group()
VISION_DISTANCE = 500
enemys_group.add(tank_enemy1, tank_enemy2, tank_enemy3)
player_bullet_group = sprite.Group()
player_group = pygame.sprite.Group()
player_group.add(tank_player)
enemys_bullet_group = sprite.Group()

level = [
    "0000000000000000",
    "0      0       0",
    "0 0000 0 0000  0",
    "0 0    0    0  0",
    "0 0 0000000 0  0",
    "0 0       0 0  0",
    "0 000 000 0 0  0",
    "0    0   0   0 0",
    "0 0000 0 0000  0",
    "0      0       0",
    "0  0000000000  0",
    "0000000000000000"]

walls = sprite.Group()
x = 0
y = 0
for ent in level:
    x = 0
    for e in ent:
        if e == "0":
            wall = GSprite(img_wall, x, y, 50, 0)
            walls.add(wall)
        x += 50
    y += 50


game = True
clock = time.Clock()
FPS = 60
kill_count = 0
game_over = False

def menu():
    menu_run = True

    while menu_run:
        window.blit(background, (0, 0))

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        draw_text("КРУТІ ТАНЧИКИ", 64, (255, 255, 255), 400, 150)

        font_play = font.Font(None, 45)
        play_text = font_play.render("У БІЙ", True, (255, 255, 255))
        play_rect = play_text.get_rect(center=(400, 280))

        if play_rect.collidepoint(mouse_pos):
            play_text = font_play.render("У БІЙ", True, (200, 200, 200))
            if mouse_click[0]:
                return True
        window.blit(play_text, play_rect)

        font_exit = font.Font(None, 45)
        exit_text = font_exit.render("ПОКИНУТИ ГРУ", True, (255, 255, 255))
        exit_rect = exit_text.get_rect(center=(400, 360))

        if exit_rect.collidepoint(mouse_pos):
            exit_text = font_exit.render("ПОКИНУТИ ГРУ", True, (200, 200, 200))
            if mouse_click[0]:
                pygame.quit()
                exit()
        window.blit(exit_text, exit_rect)

        for e in event.get():
            if e.type == QUIT:
                pygame.quit()
                exit()

        display.update()
        clock.tick(60)

if menu():
    game = True
else:
    game = False

while game:    
    for e in event.get():
        if e.type == QUIT:
            game = False

    if kill_count >= 3:
        draw_text("ВИ ПЕРЕМОГЛИ", 80, (255, 255, 255), 400, 300)
        display.update()
        pygame.time.delay(3000)
        game = False
        menu()

    if game_over:
        draw_text("МАШИНА ЗНИЩЕНА", 80, (255, 255, 255), 400, 300)
        display.update()
        pygame.time.delay(3000)
        game = False
        menu()

    window.blit(background, (0,0) )
    window.blit(tank_player.image, tank_player.rect)
    player_bullet_group.draw(window)
    player_bullet_group.update()
    enemys_bullet_group.draw(window)
    enemys_bullet_group.update()
    enemys_group.draw(window)
    for enemy in enemys_group:
        enemy.update()
        enemy.shoot()
    for player in player_group:
        tank_player.movement()
        tank_player.shoot()
        tank_player.collision(walls)
    for enemy in enemys_group:
        enemy.detected = False

        dx = tank_player.rect.centerx - enemy.rect.centerx
        dy = tank_player.rect.centery - enemy.rect.centery
        distance = m.hypot(dx, dy)
        

        if distance < VISION_DISTANCE:
            line = (enemy.rect.centerx, enemy.rect.centery, tank_player.rect.centerx, tank_player.rect.centery)
            blocked = False
            for wall in walls:
                if wall.rect.clipline(line):
                    blocked = True
                    break

            if not blocked:
                enemy.detected = True
                

    for wall in walls:
        wall.reset()
   

    display.update()
    clock.tick(FPS)