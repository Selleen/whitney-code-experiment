import pygame
import math
import random

average_h = 0
average_v = 0
sprite_list = []

class Sprite:
    def __init__(self, sprite_num):
        self.sprite_num = sprite_num
        self.visible = random.choice([True, False])
        self.angle = random.randint(0, 360)
        self.start_h = random.randint(75, 515)
        self.start_v = random.randint(75, 355)
        self.angle_vector = random.choice([-1, 1])
        self.loc_h = self.start_h
        self.loc_v = self.start_v
        self.diameter = 0
        self.angle_step = 0

    def move(self):
        angle_rad = 2.0 * math.pi * self.angle / 360.0
        delta_x = math.cos(angle_rad)
        delta_y = math.sin(angle_rad)
        self.loc_h = self.start_h + (delta_x * self.diameter)
        self.loc_v = self.start_v + (delta_y * self.diameter)

    def check_intersect(self, average_h, average_v):
        if abs(self.loc_h - average_h) < 2 and abs(self.loc_v - average_v) < 2:
            self.angle_vector = 0

    def report_status(self):
        return self.angle_vector


def calculate_constants():
    global average_h, average_v, sprite_list

    if not sprite_list:
        return False

    sum_h = 0
    sum_v = 0
    visible_sprites = [sprite for sprite in sprite_list if sprite.visible]

    if not visible_sprites:
        return False

    for sprite in visible_sprites:
        sum_h += sprite.start_h
        sum_v += sprite.start_v

    count = len(visible_sprites)
    average_h = sum_h / count
    average_v = sum_v / count

    for sprite in visible_sprites:
        dif_h = abs(sprite.start_h - average_h)
        dif_v = abs(sprite.start_v - average_v)
        sprite.diameter = math.sqrt(dif_h**2 + dif_v**2)
        sprite.angle_step = sprite.diameter / 100.0
        sprite.angle_step = max(0.75, min(sprite.angle_step, 2.5))
    return True


def check_done():
    global sprite_list

    done_flag = any(sprite.report_status() != 0 for sprite in sprite_list)

    if not done_flag:
        sprite_list = []
        return True
    return False


def main():
    global sprite_list

    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Lingo Transpiled Example")
    clock = pygame.time.Clock()
    sprite_list = [Sprite(i) for i in range(10)]
    running = True
    while running:
        screen.fill((0, 0, 0))

        if not calculate_constants():
            running = False

        for sprite in sprite_list:
            if sprite.visible:
                sprite.move()
                sprite.check_intersect(average_h, average_v)
                pygame.draw.circle(screen, (255, 255, 255), (int(sprite.loc_h), int(sprite.loc_v)), 5)
                
                sprite.angle += sprite.angle_step * sprite.angle_vector
                if abs(sprite.angle) > 360 * 7:
                    screen.fill((200, 200, 0))
                    pygame.display.flip()
                    pygame.time.delay(1500)
                    running = False

        if check_done():
            screen.fill((200, 200, 0))
            pygame.display.flip()
            pygame.time.delay(1500)
            running = False

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()
