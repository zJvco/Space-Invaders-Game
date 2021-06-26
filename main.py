import pygame
import os
import sys
import random
from math import sqrt

# Start pygame modules
pygame.init()

# Creante the Window
width, height = 800, 600
window = pygame.display.set_mode((width, height))

# Títle and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load(os.path.join("assets", "planet-earth.png"))
pygame.display.set_icon(icon)

# Colors
WHITE = (255, 255, 255)

def main():
    clock = pygame.time.Clock()


    def player(img, x, y):
        window.blit(img, (x, y))


    def enemy(img, x, y):
        window.blit(img, (x, y))


    def bullet(img, color):
        pygame.draw.rect(window, color, img)


    def collision(bx, by, ex, ey):
        distance = sqrt(((bx - ex)**2) + ((by - ey)**2))

        if distance < enemy_width:
            return True
        else:
            return False


    def drawFont(font):
        score_label = font.render(f"Score: {score}", 1, WHITE)
        window.blit(score_label, (10, 10))

        level_up = font.render(f"Level: {level}", 1, WHITE)
        window.blit(level_up, (width - level_up.get_width() - 10, 10))


    # Player Requirements
    player_ship = pygame.image.load(os.path.join("assets", "space-ship.png"))
    player_x = width/2 - player_ship.get_width()/2
    player_y = height/2 - player_ship.get_height()/2 + 250
    player_speed = 5

    # Enemy Requirements
    enemy_alien = []
    enemy_x = []
    enemy_y = []
    enemy_width = 50
    enemy_height = 50
    enemy_speed = []
    num_enemies = 5

    # Bullet Requirements
    bullet_width = 5
    bullet_heith = 20
    bullet_x = 0
    bullet_y = player_y - 20
    bullet_speed = 10
    bullet_state = False
    bullet_color = (231, 76, 60)

    # BG
    background = pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "background.png")))

    # Font
    font = pygame.font.SysFont("comicsans", 25)

    score = 0
    level = 0
    FPS = 60

    # Screen Loop
    while True:
        window.blit(background, (0, 0))
        clock.tick(FPS)

        for e in range(num_enemies):
            enemy_alien.append(pygame.transform.scale(pygame.image.load(os.path.join("assets", "alien.png")), (enemy_width, enemy_height)))
            enemy_x.append(random.randint(enemy_width, width - enemy_width))
            enemy_y.append(random.randint(50, 150))
            enemy_speed.append(3)
        
        current_bullet_x = player_x + player_ship.get_width()/2 - bullet_width/2

        drawFont(font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and player_x <= width - player_ship.get_width():
            player_x += player_speed
        if keys[pygame.K_LEFT] and player_x >= 0:
            player_x -= player_speed
        if keys[pygame.K_SPACE] and not bullet_state:
            bullet_x = current_bullet_x
            bullet_state = True

        for e in range(num_enemies):
            enemy_x[e] += enemy_speed[e]

            if enemy_x[e] <= 0 or enemy_x[e] >= width - enemy_width:
                enemy_speed[e] *= -1
                enemy_y[e] += enemy_height

            if collision(bullet_x, bullet_y, enemy_x[e], enemy_y[e]):
                bullet_y = player_y - 20
                bullet_state = False
                enemy_x[e] = (random.randint(enemy_width, width - enemy_width))
                enemy_y[e] = (random.randint(50, 150))
                score += 1

            enemy(enemy_alien[e], enemy_x[e], enemy_y[e])

        player(player_ship, player_x, player_y)

        bullet_img = pygame.Rect(bullet_x, bullet_y, bullet_width, bullet_heith)

        if bullet_y <= 0:
            bullet_y = player_y - 20
            bullet_state = False

        if bullet_state:
            bullet(bullet_img, bullet_color)
            bullet_y -= bullet_speed

        if score == num_enemies:
            num_enemies += 5
            level += 1
            score = 0
            
        pygame.display.update()


if __name__ == "__main__":
    main()
