import pygame
import os

pygame.init()
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Battle")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

NORMAL_FONT = pygame.font.SysFont('comicsans', 100)
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WIN_FONT = pygame.font.SysFont('comicsans', 100)

BORDER = pygame.Rect(WIDTH//2-5, 0, 10, HEIGHT)

FPS = 60
VEL = 5
BULLET_VEL = 8
NUM_BULLET = 5

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 60, 55

PLAYER_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'player_hit.mp3'))
BULLET_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'spawn_bullet.mp3'))
GAME_OVER = pygame.mixer.Sound(os.path.join('Assets', 'game_over.mp3'))

SPACESHIP_YELLOW_PIC = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
SPACESHIP_YELLOW = pygame.transform.rotate(pygame.transform.scale(
    SPACESHIP_YELLOW_PIC, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

SPACESHIP_RED_PIC = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
SPACESHIP_RED = pygame.transform.rotate(pygame.transform.scale(
    SPACESHIP_RED_PIC, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), -90)

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join("Assets", "space.png")), (WIDTH, HEIGHT))


def handle_yellow_movement(key_pressed, yellow):
    if key_pressed[pygame.K_a] and yellow.x - VEL > 0:  # LEFT
        yellow.x -= VEL
    if key_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:  # RIGHT
        yellow.x += VEL
    if key_pressed[pygame.K_w] and yellow.y - VEL > 0:  # UP
        yellow.y -= VEL
    if key_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT:  # DOWN
        yellow.y += VEL


def handle_red_movement(key_pressed, red):
    if key_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # LEFT
        red.x -= VEL
    if key_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  # RIGHT
        red.x += VEL
    if key_pressed[pygame.K_UP] and red.y - VEL > 0:  # UP
        red.y -= VEL
    if key_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT:  # DOWN
        red.y += VEL


def handle_bullet_movement(yellow_bullets, red_bullets, yellow, red):

    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
            PLAYER_HIT_SOUND.play()

        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
            PLAYER_HIT_SOUND.play()

        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WIN_FONT.render(text, 1, YELLOW)
    GAME_OVER.play()
    WIN.blit(SPACE, (0, 0))
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width() //
                         2, HEIGHT/2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)


def draw_window(yellow, red, yellow_bullets, red_bullets, yellow_health, red_health, max_health):

    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, WHITE, BORDER)

    pygame.draw.rect(WIN, WHITE, (10, 10, 200, 20))
    pygame.draw.rect(WIN, YELLOW, (15, 15,187*(yellow_health/max_health), 10))

    pygame.draw.rect(WIN, WHITE, (WIDTH - 200 -10, 10, 200, 20))
    pygame.draw.rect(WIN, RED, (WIDTH - 200 -4, 15,187*(red_health/max_health), 10))

    WIN.blit(SPACESHIP_YELLOW, (yellow.x, yellow.y))
    WIN.blit(SPACESHIP_RED, (red.x, red.y))

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    pygame.display.update()


def main():

    clock = pygame.time.Clock()

    yellow = pygame.Rect(200, 250, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red = pygame.Rect(700, 250, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    yellow_bullets = []
    red_bullets = []

    max_health = 20
    yellow_health = 20
    red_health = 20

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < NUM_BULLET:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < NUM_BULLET:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1

            if event.type == RED_HIT:
                red_health -= 1

        winner_text = ""
        if yellow_health == 0:
            winner_text = "Red Won!"
        if red_health == 0:
            winner_text = "Yellow Won!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        key_pressed = pygame.key.get_pressed()

        handle_yellow_movement(key_pressed, yellow)
        handle_red_movement(key_pressed, red)

        handle_bullet_movement(yellow_bullets, red_bullets, yellow, red)

        draw_window(yellow, red, yellow_bullets,
                    red_bullets, yellow_health, red_health, max_health)

    main_menu()


STATE_FONT = pygame.font.SysFont("comicsans", 35)


def main_menu():

    state = "start"
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    state = "start"
                if event.key == pygame.K_DOWN:
                    state = "quit"
                if event.key == pygame.K_RETURN:
                    if state == "start":
                        main()
                    if state == "quit":
                        quit()

        WIN.blit(SPACE, (0, 0))

        text = NORMAL_FONT.render("SPACE BATTLE", 1, YELLOW)
        pygame.draw.rect(WIN, YELLOW, (WIDTH//2 - text.get_width()//2, HEIGHT //
                                       2 - text.get_height() - 60, text.get_width()+10, text.get_height()+10), 3)
        WIN.blit(text, (WIDTH//2 - text.get_width()//2 +
                        5, HEIGHT//2 - text.get_height() - 50))

        start_text = STATE_FONT.render("START", 1, YELLOW)
        WIN.blit(start_text, (WIDTH//2 - start_text.get_width() //
                              2, HEIGHT//2 - text.get_height()//2 + 30))

        quit_text = STATE_FONT.render("QUIT", 1, YELLOW)
        WIN.blit(quit_text, (WIDTH//2 - start_text.get_width() //
                             2+7, HEIGHT//2 - text.get_height()//2 + 70))

        if state == "start":
            pygame.draw.rect(WIN, YELLOW, (WIDTH//2 - start_text.get_width()//2 - 10, HEIGHT//2 -
                                           text.get_height()//2 + 23, start_text.get_width()+20, start_text.get_height()+10), 3)
        elif state == "quit":
            pygame.draw.rect(WIN, YELLOW, (WIDTH//2 - start_text.get_width()//2 - 10, HEIGHT//2 -
                                           text.get_height()//2 + 65, start_text.get_width()+20, start_text.get_height()+10), 3)

        pygame.display.update()


if __name__ == '__main__':
    main_menu()
