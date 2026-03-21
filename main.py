from pygame import *

class GSprite(sprite.Sprite):
    def __init__(self, entity_img, entity_pos_x, entity_pos_y, entity_size, entity_speed):
        super().__init__()
        self.image = transform.scale(image.load(entity_img), (entity_size, entity_size))
        self.speed = entity_speed
        self.rect.x = entity_pos_x
        self.rect.y = entity_pos_y

class Player(GSprite):
    def __init__(self, entity_img, entity_pos_x, entity_pos_y, entity_speed):
        super().__init__(entity_img, entity_pos_x, entity_pos_y, entity_speed)

class Enemy(GSprite):
    pass



window = display.set_mode((800, 600))
display.set_caption("Круті танчики")
background = transform.scale(image.load("testbg.png"), (800, 600))


game = True
clock = time.Clock()
FPS = 60

while game:    
    for e in event.get():
        if e.type == QUIT:
            game = False

    window.blit(background, (0, 0))


    display.update()
    clock.tick(FPS)