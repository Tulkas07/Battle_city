import pygame
from pygame import *

pygame.init()

img_player = "player_tank_sprite.png"
img_enemy = "enemy_tank_sprite.png"
img_wall = "wall_sprite.png"



class GSprite(sprite.Sprite):
    def __init__(self, entity_img, entity_pos_x, entity_pos_y, entity_size, entity_speed):
        super().__init__()
        self.image = transform.scale(image.load(entity_img), (entity_size, entity_size))
        self.rect = self.image.get_rect()
        self.speed = entity_speed
        self.rect.x = entity_pos_x
        self.rect.y = entity_pos_y
        

class Player(GSprite):
    def __init__(self, entity_img, entity_pos_x, entity_pos_y, entity_size,  entity_speed):
        super().__init__(entity_img, entity_pos_x, entity_pos_y, entity_size, entity_speed)
        self.direction = "UP"

    
    def movement(self):
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
                
    def collision(self):
        pass
        


class Enemy(GSprite):
    pass



window = display.set_mode((800, 600))
display.set_caption("Круті танчики")
background = transform.scale(image.load("background.png"), (800, 600))
tank_player = Player(img_player, 0, 0, 65, 3)

game = True
clock = time.Clock()
FPS = 60

while game:    
    for e in event.get():
        if e.type == QUIT:
            game = False

    window.blit(background, (0,0) )
    window.blit(tank_player.image, tank_player.rect)
    tank_player.movement()

    display.update()
    clock.tick(FPS)
