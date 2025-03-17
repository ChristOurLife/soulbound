import pygame
import sys
import random
import time

# Initialize
pygame.init()

# Initial screen size
screen_width, screen_height = 1080, 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Difficulty Scaling Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Player setup
player = pygame.Rect(300, 400, 50, 50)
player_speed = 400

# Enemy setup
enemy_speed = 150
enemies = [pygame.Rect(random.randint(0, screen_width-50), random.randint(0, screen_height-50), 50, 50)]

# Power-up setup
powerups = []
powerup_spawn_time = 5  # Initial power-up spawn interval (seconds)
last_powerup_spawn = time.time()

# Health setup
player_health = 100
max_health = 100
max_health_counter = 0

# Difficulty scaling
start_time = time.time()
scaling_interval = 10  # Increase difficulty every 10 seconds
next_scale = start_time + scaling_interval

# Clock
clock = pygame.time.Clock()

def draw_health_bar(surface, x, y, health, max_health):
    health_ratio = health / max_health
    bar_width = max_health * 2  # Scale bar width with max health
    bar_height = 20
    pygame.draw.rect(surface, RED, (x, y, bar_width, bar_height))
    pygame.draw.rect(surface, GREEN, (x, y, bar_width * health_ratio, bar_height))

def move_enemy(enemy, target, dt):
    if enemy.x < target.x:
        enemy.x += enemy_speed * dt
    if enemy.x > target.x:
        enemy.x -= enemy_speed * dt
    if enemy.y < target.y:
        enemy.y += enemy_speed * dt
    if enemy.y > target.y:
        enemy.y -= enemy_speed * dt

def spawn_powerup():
    x = random.randint(0, screen_width - 30)
    y = random.randint(0, screen_height - 30)
    return pygame.Rect(x, y, 30, 30)

running = True
while running:
    dt = clock.tick(60) / 1000  # Delta time in seconds
    current_time = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= player_speed * dt
    if keys[pygame.K_RIGHT]:
        player.x += player_speed * dt
    if keys[pygame.K_UP]:
        player.y -= player_speed * dt
    if keys[pygame.K_DOWN]:
        player.y += player_speed * dt

    # Move enemies and check collision
    for enemy in enemies:
        move_enemy(enemy, player, dt)
        if player.colliderect(enemy):
            player_health -= 30 * dt
            if player_health <= 0:
                print("You died!")
                running = False

    # Spawn power-ups over time
    if current_time - last_powerup_spawn >= powerup_spawn_time:
        powerups.append(spawn_powerup())
        last_powerup_spawn = current_time

    # Check power-up collection
    for powerup in powerups[:]:
        if player.colliderect(powerup):
            max_health += 100
            player_health = min(player_health + 10, max_health)
            powerups.remove(powerup)

    # Difficulty scaling
    if current_time >= next_scale:
        enemy_speed += 20  # Increase enemy speed
        if powerup_spawn_time > 2:
            powerup_spawn_time -= 0.5  # Reduce power-up frequency
        enemies.append(pygame.Rect(random.randint(0, screen_width-50), random.randint(0, screen_height-50), 50, 50))
        next_scale += scaling_interval

    # Drawing
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, player)

    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy)

    for powerup in powerups:
        pygame.draw.rect(screen, BLUE, powerup)

    draw_health_bar(screen, 20, 20, player_health, max_health)

    pygame.display.flip()

pygame.quit()
