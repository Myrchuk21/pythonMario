import pygame
import sys

# Инициализация Pygame
pygame.init()

# Константы экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mario-style Game")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Музыка
pygame.mixer.music.load("music/menu-music.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)

# Переменные
volume = 0.5
player_color = BLUE
game_running = False

# Параметры игрока
player = pygame.Rect(100, 500, 50, 50)
velocity_x = 0
velocity_y = 0
gravitiy = 0.5
jump = False
speed = 5

# Платформы
platforms = [
    pygame.Rect(0, 550, 800, 50),
    pygame.Rect(200, 450, 200, 20),
    pygame.Rect(500, 350, 200, 20)
]

# Загрузка фона
background = pygame.image.load("image/background.jpg").convert()  # Подставьте ваш путь к изображению

# Растягиваем фон на весь экран
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Функции для меню
def draw_text(text, size, x, y, color=WHITE):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def main_menu():
    global game_running
    pygame.mixer.music.set_volume(volume * 0.5)
    while True:
        screen.fill(BLACK)
        draw_text("Main Menu", 50, 300, 50)
        draw_text("[1] Start Game", 40, 300, 150)
        draw_text("[2] Settings", 40, 300, 250)
        draw_text("[3] Change Character", 40, 300, 350)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    game_running = True
                    pygame.mixer.music.set_volume(volume)
                    return
                if event.key == pygame.K_2:
                    settings_menu()
                if event.key == pygame.K_3:
                    change_character()

def settings_menu():
    global volume
    while True:
        screen.fill(BLACK)
        draw_text("Settings", 50, 300, 50)
        draw_text(f"Volume: {int(volume * 100)}%", 40, 300, 150)
        draw_text("Press UP to increase volume", 30, 200, 200)
        draw_text("Press DOWN to decrease volume", 30, 200, 250)
        draw_text("Press ESC to return", 30, 200, 300)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    volume = min(1.0, volume + 0.1)
                    pygame.mixer.music.set_volume(volume * 0.5)
                if event.key == pygame.K_DOWN:
                    volume = max(0.0, volume - 0.1)
                    pygame.mixer.music.set_volume(volume * 0.5)
                if event.key == pygame.K_ESCAPE:
                    return

def change_character():
    global player_color
    while True:
        screen.fill(BLACK)
        draw_text("Change Character", 50, 250, 50)
        draw_text("Press R for Red, B for Blue", 30, 200, 200)
        draw_text("Press ESC to return", 30, 200, 300)
        pygame.draw.rect(screen, player_color, (350, 400, 50, 50))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    player_color = RED
                if event.key == pygame.K_b:
                    player_color = BLUE
                if event.key == pygame.K_ESCAPE:
                    return

def game_loop():
    global player_color, velocity_x, velocity_y, jump
    clock = pygame.time.Clock()
    while game_running:
        # Отображаем задний фон, растянутый на весь экран
        screen.blit(background, (0, 0))

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    velocity_x = -speed
                if event.key == pygame.K_RIGHT:
                    velocity_x = speed
                if event.key == pygame.K_SPACE and not jump:
                    velocity_y = -10
                    jump = True
            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    velocity_x = 0

        # Движение игрока
        player.x += velocity_x
        velocity_y += gravitiy
        player.y += velocity_y

        # Проверка коллизий с платформами
        for platform in platforms:
            if player.colliderect(platform) and velocity_y > 0:
                player.y = platform.y - player.height
                velocity_y = 0
                jump = False

        # Отрисовка
        pygame.draw.rect(screen, player_color, player)
        for platform in platforms:
            pygame.draw.rect(screen, GREEN, platform)
        pygame.display.flip()
        clock.tick(60)

# Запуск игры
main_menu()
game_loop()
