import pygame
import os
import sys
import random
from math import sqrt
from pygame import mixer
from menu import Menu

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
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)


def main():
    clock = pygame.time.Clock()

    def player(img, x, y):
        window.blit(img, (x, y))

    def enemy(img, x, y):
        window.blit(img, (x, y))

    def bullet(img, color):
        pygame.draw.rect(window, color, img)

    def helth(bar_img, life_img, white, green):
        pygame.draw.rect(window, white, bar_img)
        pygame.draw.rect(window, green, life_img)

    def collision(Ax, Ay, Bx, By):
        # Pitágoras Formula to Calculate the Distance Between Two Points. D = sqrt((Ax - Bx)**2 + (Ay - By)**2))
        distance = sqrt((Ax - (Bx + enemy_width/2))**2 + (Ay - By)**2)

        if distance < 50:
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

    # Helth
    current_life = player_ship.get_width()

    # Game Over
    game_over = False

    # Background Image
    background = pygame.transform.scale2x(
        pygame.image.load(os.path.join("assets", "background.png")))

    # Font
    font = pygame.font.SysFont("comicsans", 25)

    # Background Sound
    mixer.music.load(os.path.join("assets", "Background-Music.mp3"))
    mixer.music.play(-1)
    mixer.music.set_volume(0.2)

    # Bullet Sound
    bullet_sound = mixer.Sound(os.path.join("assets", "Laser_Sound.mp3"))

    # Explosion Sound
    explosion_sound = mixer.Sound(
        os.path.join("assets", "Explosion_Sound.wav"))

    score = 0
    level = 0
    FPS = 60

    # Screen Loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if not game_over:
            window.blit(background, (0, 0))
            current_bullet_x = player_x + player_ship.get_width()/2 - bullet_width/2

            for e in range(num_enemies):
                enemy_alien.append(pygame.transform.scale(pygame.image.load(
                    os.path.join("assets", "alien.png")), (enemy_width, enemy_height)))
                enemy_x.append(random.randint(enemy_width, width - enemy_width))
                enemy_y.append(random.randint(50, 150))
                enemy_speed.append(3)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT] and player_x <= width - player_ship.get_width():
                player_x += player_speed
            if keys[pygame.K_LEFT] and player_x >= 0:
                player_x -= player_speed

            if keys[pygame.K_SPACE] and not bullet_state:
                bullet_sound.play()
                bullet_x = current_bullet_x
                bullet_state = True

            for e in range(num_enemies):
                enemy_x[e] += enemy_speed[e]

                if enemy_x[e] <= 0 or enemy_x[e] >= width - enemy_width:
                    enemy_speed[e] *= -1
                    enemy_y[e] += enemy_height

                if collision(bullet_x, bullet_y, enemy_x[e], enemy_y[e]):
                    explosion_sound.play()
                    bullet_x = -100
                    bullet_y = player_y - 20
                    bullet_state = False
                    enemy_x[e] = (random.randint(enemy_width, width - enemy_width))
                    enemy_y[e] = (random.randint(50, 150))
                    score += 1

                if collision(player_x, player_y, enemy_x[e], enemy_y[e]):
                    explosion_sound.play()
                    current_life -= 8
                    enemy_alien.pop(e)
                    enemy_x.pop(e)
                    enemy_y.pop(e)
                    enemy_speed.pop(e)

                enemy(enemy_alien[e], enemy_x[e], enemy_y[e])

            player(player_ship, player_x, player_y)
            drawFont(font)

            bullet_img = pygame.Rect(
                bullet_x, bullet_y, bullet_width, bullet_heith)
            helth_bar_img = pygame.Rect(
                player_x, player_y + player_ship.get_height(), player_ship.get_width(), 6)
            current_life_img = pygame.Rect(player_x, player_y + player_ship.get_height(), current_life, 6)

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

            helth(helth_bar_img, current_life_img, WHITE, GREEN)

            if current_life <= 0:
                game_over = True
                window.fill(BLACK)
        else:
            menu = Menu()

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
