import pygame
import os
import sys
import random
from math import sqrt
from pygame import mixer

# Start pygame modules
pygame.init()

# Creante the Window
width, height = 800, 600
window = pygame.display.set_mode((width, height))

# Títle and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load(os.path.join("assets", "space-invaders-logo.png"))
pygame.display.set_icon(icon)

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)
YELLOW = (245, 176, 65)


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

        if distance < enemy_height:
            return True
        else:
            return False

    def drawFont(font):
        score_label = font.render(f"Score: {score}", 1, WHITE)
        window.blit(score_label, (10, 10))

        level_up = font.render(f"Level: {level}", 1, WHITE)
        window.blit(level_up, (width - level_up.get_width() - 10, 10))

    def remove_enemy(e):
        enemy_alien.pop(e)
        enemy_x.pop(e)
        enemy_y.pop(e)
        enemy_speed.pop(e)

    def menu_polygon_move(p1_x, p1_y, p2_x, p2_y, p3_x, p3_y, color):
        pygame.draw.polygon(
            window, color, [(p1_x, p1_y), (p2_x, p2_y), (p3_x, p3_y)])

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
    enemy_height = 32
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
    game_stage = "MENU"

    # Background Image
    background = pygame.transform.scale2x(
        pygame.image.load(os.path.join("assets", "background-space.png")))

    # Font
    font = pygame.font.SysFont("comicsans", 25)
    menu_font = pygame.font.SysFont("comicsans", 50)

    # Background Sound
    mixer.music.load(os.path.join("assets", "Background-Music.mp3"))
    mixer.music.play(-1)
    mixer.music.set_volume(0.2)

    # Bullet Sound
    bullet_sound = mixer.Sound(os.path.join("assets", "Laser_Sound.mp3"))

    # Explosion Sound
    explosion_sound = mixer.Sound(
        os.path.join("assets", "Explosion_Sound.wav"))

    # Level-up Sound
    level_up_sound = mixer.Sound(os.path.join("assets", "sound_correct.wav"))



    # Menu Variables / Requeriments
    menu_logo = pygame.transform.scale(pygame.image.load(os.path.join("assets", "space-invaders-logo.png")), (400, 330))
    start_label = menu_font.render("START", 1, WHITE)
    options_label = menu_font.render("OPTIONS", 1, WHITE)
    exit_label = menu_font.render("EXIT GAME", 1, WHITE)
    credits_label = font.render("Created by João Victor. All rights reserved", 0, WHITE)

    pos1_x = width/2 - 150
    pos1_y = height/2 + 25
    pos2_x = width/2 - 150
    pos2_y = height/2 + 5
    pos3_x = width/2 - 150 + 20
    pos3_y = height/2 + 15
    current_menu_label = 0

    # Options Menu
    arrow_right_text = font.render("ARROW RIGHT: Move ship right", 1, WHITE)
    arrow_left_text = font.render("ARROW LEFT: Move ship left", 1, WHITE)
    backspace_text = font.render("BACKSPACE: Ship shooting", 1, WHITE)
    back_label = menu_font.render("BACK", 1, WHITE)
    



    score = 0
    level = 0
    FPS = 60

    # Screen Loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if game_stage == "MENU":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        if current_menu_label >= 2:
                            current_menu_label = 0
                        else:
                            current_menu_label += 1
                    if event.key == pygame.K_UP:
                        if current_menu_label <= 0:
                            current_menu_label = 2
                        else:
                            current_menu_label -= 1

                    if event.key == pygame.K_RETURN:
                        if current_menu_label == 0:
                            game_stage = "GAME"
                        elif current_menu_label == 1:
                            game_stage = "OPTIONS"
                        else:
                            pygame.quit()
                            sys.exit()
            elif game_stage == "OPTIONS":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_stage = "MENU"

        if game_stage == "MENU": # MENU
            window.blit(background, (0, 0))

            window.blit(menu_logo, (width/2 - menu_logo.get_width()/2, -50))
            window.blit(start_label, (width/2 - start_label.get_width()/2, height/2))
            window.blit(options_label, (width/2 - options_label.get_width()/2, height/2 + 60))
            window.blit(exit_label, (width/2 - exit_label.get_width()/2, height/2 + 120))
            window.blit(credits_label, (width/2 - credits_label.get_width()/2, height - 25))

            if current_menu_label == 0:
                pos1_x = width/2 - 150
                pos1_y = height/2 + 25
                pos2_x = width/2 - 150
                pos2_y = height/2 + 5
                pos3_x = width/2 - 150 + 20
                pos3_y = height/2 + 15
            elif current_menu_label == 1:
                pos1_x = width/2 - 150
                pos1_y = height/2 + 85
                pos2_x = width/2 - 150
                pos2_y = height/2 + 65
                pos3_x = width/2 - 150 + 20
                pos3_y = height/2 + 75
            else:
                pos1_x = width/2 - 150
                pos1_y = height/2 + 145
                pos2_x = width/2 - 150
                pos2_y = height/2 + 125
                pos3_x = width/2 - 150 + 20
                pos3_y = height/2 + 135

            menu_polygon_move(pos1_x, pos1_y, pos2_x, pos2_y, pos3_x, pos3_y, YELLOW)
        elif game_stage == "GAME": # GAME
            mixer.music.stop()
            window.blit(background, (0, 0))
            current_bullet_x = player_x + player_ship.get_width()/2 - bullet_width/2

            for e in range(num_enemies):
                enemy_alien.append(pygame.transform.scale(pygame.image.load(
                    os.path.join("assets", "alien-invader.png")), (enemy_width, enemy_height)))
                enemy_x.append(random.randint(
                    enemy_width, width - enemy_width))
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
                    bullet_x = -1000
                    bullet_y = player_y - 20
                    bullet_state = False
                    score += 1
                    remove_enemy(e)

                if collision(player_x, player_y, enemy_x[e], enemy_y[e]):
                    explosion_sound.play()
                    current_life -= 8
                    remove_enemy(e)

                enemy(enemy_alien[e], enemy_x[e], enemy_y[e])

            player(player_ship, player_x, player_y)
            drawFont(font)

            bullet_img = pygame.Rect(
                bullet_x, bullet_y, bullet_width, bullet_heith)
            helth_bar_img = pygame.Rect(
                player_x, player_y + player_ship.get_height(), player_ship.get_width(), 5)
            current_life_img = pygame.Rect(
                player_x, player_y + player_ship.get_height(), current_life, 5)

            if bullet_y <= 0:
                bullet_y = player_y - 20
                bullet_state = False

            if bullet_state:
                bullet(bullet_img, bullet_color)
                bullet_y -= bullet_speed

            if score == num_enemies:
                level_up_sound.play()
                num_enemies += 5
                level += 1
                score = 0

            helth(helth_bar_img, current_life_img, WHITE, GREEN)

            if current_life <= 0:
                current_life = player_ship.get_width()
                enemy_alien.clear()
                enemy_x.clear()
                enemy_y.clear()
                enemy_speed.clear()
                num_enemies = 5
                level = 0
                score = 0
                game_stage = "MENU"
                mixer.music.play()
        elif game_stage == "OPTIONS": # OPTIONS
            window.blit(background, (0, 0))
            window.blit(menu_logo, (width/2 - menu_logo.get_width()/2, -50))
            window.blit(arrow_right_text, (width/2 - arrow_right_text.get_width()/2, height/2 - 50))
            window.blit(arrow_left_text, (width/2 - arrow_left_text.get_width()/2, height/2))
            window.blit(backspace_text, (width/2 - backspace_text.get_width()/2, height/2 + 50))
            window.blit(back_label, (width/2 - back_label.get_width()/2, height/2 + 180))
            window.blit(credits_label, (width/2 - credits_label.get_width()/2, height - 25))

            menu_polygon_move(width/2 - 100, height/2 + 205, width/2 - 100, height/2 + 185, width/2 - 100 + 20, height/2 + 195, YELLOW)

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()