import pygame
import random

# Initialize Pygame
pygame.init()

# Screen setup
screen_size = [360, 600]
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Advanced Planet Shooting Game")

# Load assets
def load_image(filename, scale=None):
    try:
        image = pygame.image.load(filename).convert_alpha()
        if scale:
            image = pygame.transform.scale(image, scale)
        return image
    except pygame.error as e:
        print(f"Error loading {filename}: {e}")
        pygame.quit()
        exit()

background = load_image('background.png', screen_size)
spaceship_image = load_image('spaceship.png', (50, 50))
bullet_image = load_image('bullet.png', (10, 20))
planet_images = [
    load_image('one.png', (60, 60)),
    load_image('planet1.png', (60, 60)),
    load_image('planet2.png', (60, 60))
]
powerup_image = load_image('powerup.png', (30, 30))

# Fonts and sounds
font = pygame.font.Font(None, 36)
pygame.mixer.init()
shoot_sound = pygame.mixer.Sound('shoot.wav')
hit_sound = pygame.mixer.Sound('hit.wav')
powerup_sound = pygame.mixer.Sound('powerup.wav')
game_over_sound = pygame.mixer.Sound('gameover.wav')

# Background music
try:
    pygame.mixer.music.load('background_music.mp3')  # Replace with your .mp3 file
    pygame.mixer.music.set_volume(0.5)  # Adjust volume (0.0 to 1.0)
    pygame.mixer.music.play(-1)  # Play in an infinite loop
except pygame.error as e:
    print(f"Error loading background music: {e}")
    pygame.quit()
    exit()

# Variables
spaceship_x = 160
spaceship_y = 500
spaceship_speed = 5

bullet_x = 0
bullet_y = 0
bullet_fired = False
bullet_speed = 8

planet_x = 140
planet_y = 50
move_direction = 1
planet_speed = 2
planet_index = 0

score = 0
lives = 3
powerups = []

# Clock for frame rate
clock = pygame.time.Clock()

# Function to draw text
def draw_text(text, x, y, size=36, color=(255, 255, 255)):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Main menu
def main_menu():
    screen.fill((0, 0, 0))
    draw_text("Planet Shooting Game", 50, 200, size=48, color=(255, 255, 0))
    draw_text("Press ENTER to Start", 70, 300)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False

# Game loop
running = True
main_menu()
while running:
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not bullet_fired:
            bullet_fired = True
            bullet_x = spaceship_x + spaceship_image.get_width() // 2 - bullet_image.get_width() // 2
            bullet_y = spaceship_y
            shoot_sound.play()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and spaceship_x > 0:
        spaceship_x -= spaceship_speed
    if keys[pygame.K_RIGHT] and spaceship_x < screen_size[0] - spaceship_image.get_width():
        spaceship_x += spaceship_speed

    planet_x += move_direction * planet_speed
    if planet_x <= 0 or planet_x >= screen_size[0] - planet_images[planet_index].get_width():
        move_direction *= -1

    if bullet_fired:
        bullet_y -= bullet_speed
        if bullet_y < 0:
            bullet_rect = pygame.Rect(bullet_x, bullet_y, bullet_image.get_width(), bullet_image.get_height())
            planet_rect = pygame.Rect(planet_x, planet_y, planet_images[planet_index].get_width(), planet_images[planet_index].get_height())
            if not bullet_rect.colliderect(planet_rect):
                lives -= 1
            bullet_fired = False

    planet_rect = pygame.Rect(planet_x, planet_y, planet_images[planet_index].get_width(), planet_images[planet_index].get_height())
    bullet_rect = pygame.Rect(bullet_x, bullet_y, bullet_image.get_width(), bullet_image.get_height())

    if bullet_fired and bullet_rect.colliderect(planet_rect):
        bullet_fired = False
        score += 10
        hit_sound.play()
        planet_index = (planet_index + 1) % len(planet_images)
        if score % 60 == 0:  # Increase difficulty every 60 points
            planet_speed += 1

    if random.randint(1, 350) == 1:  # 1 in 200 chance per frame for power-up
        powerups.append([random.randint(0, screen_size[0] - 30), 0])

    for powerup in powerups[:]:
        powerup[1] += 3
        if powerup[1] > screen_size[1]:
            powerups.remove(powerup)
        powerup_rect = pygame.Rect(powerup[0], powerup[1], powerup_image.get_width(), powerup_image.get_height())
        spaceship_rect = pygame.Rect(spaceship_x, spaceship_y, spaceship_image.get_width(), spaceship_image.get_height())
        if powerup_rect.colliderect(spaceship_rect):
            powerups.remove(powerup)
            powerup_sound.play()
            lives += 1

    if lives == 0:
        game_over_sound.play()
        draw_text("GAME OVER", 100, 250, size=48, color=(255, 0, 0))
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False

    screen.blit(planet_images[planet_index], (planet_x, planet_y))
    if bullet_fired:
        screen.blit(bullet_image, (bullet_x, bullet_y))
    screen.blit(spaceship_image, (spaceship_x, spaceship_y))
    for powerup in powerups:
        screen.blit(powerup_image, (powerup[0], powerup[1]))

    draw_text(f"Score: {score}", 10, 10)
    draw_text(f"Lives: {lives}", 260, 10)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
