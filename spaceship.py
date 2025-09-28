import pygame
import random
import serial

pygame.init()
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroid Dodger")

WHITE = (255, 255, 255)
BLACK = (0, 51, 103)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)

arduino_port = 'COM6'  
baud_rate = 9600
ser = serial.Serial(arduino_port, baud_rate, timeout=1)

class Rocket:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.bullets = []

class Bullet:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed

class Asteroid:
    def __init__(self, x, y, radius, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed

rocket = Rocket(WIDTH // 2, HEIGHT - 60, 40, 40, GREEN)
asteroids = []
score = 0

clock = pygame.time.Clock()
running = True

THRESHOLD_LOW = 400
THRESHOLD_HIGH = 700
ROCKET_SPEED = 7
BULLET_SPEED = 7
ASTEROID_SIZE = 40
ASTEROID_SPEED_RANGE = (2, 6)

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    try:
        line = ser.readline().decode(errors="ignore").strip()
        data = line.split(',')
        if len(data) == 3:
            joy_x, joy_y, button = map(int, data)


            if joy_x < THRESHOLD_LOW:
                rocket.x -= ROCKET_SPEED
            elif joy_x > THRESHOLD_HIGH:
                rocket.x += ROCKET_SPEED

            if joy_y < THRESHOLD_LOW:
                rocket.y -= ROCKET_SPEED
            elif joy_y > THRESHOLD_HIGH:
                rocket.y += ROCKET_SPEED

            if button == 0: 
                rocket.bullets.append(Bullet(rocket.x + rocket.width//2, rocket.y, BULLET_SPEED))
    except:
        pass


    rocket.x = max(0, min(WIDTH - rocket.width, rocket.x))
    rocket.y = max(0, min(HEIGHT - rocket.height, rocket.y))


    new_bullets = []
    for bullet in rocket.bullets:
        bullet.y -= bullet.speed
        if bullet.y > 0:
            new_bullets.append(bullet)
    rocket.bullets = new_bullets


    if random.randint(1, 30) == 1:
        ax = random.randint(0, WIDTH - ASTEROID_SIZE)
        ay = -ASTEROID_SIZE
        speed = random.randint(*ASTEROID_SPEED_RANGE)
        asteroids.append(Asteroid(ax, ay, ASTEROID_SIZE//2, speed))

    new_asteroids = []
    for asteroid in asteroids:
        asteroid.y += asteroid.speed
        if asteroid.y < HEIGHT:
            new_asteroids.append(asteroid)
    asteroids = new_asteroids


    rocket_rect = pygame.Rect(rocket.x, rocket.y, rocket.width, rocket.height)
    for asteroid in asteroids[:]:
        asteroid_rect = pygame.Rect(asteroid.x, asteroid.y, asteroid.radius*2, asteroid.radius*2)


        if rocket_rect.colliderect(asteroid_rect):
            print(" Game Over! Score:", score)
            running = False


        for bullet in rocket.bullets[:]:
            bullet_rect = pygame.Rect(bullet.x, bullet.y, 5, 10)
            if bullet_rect.colliderect(asteroid_rect):
                try:
                    asteroids.remove(asteroid)
                    rocket.bullets.remove(bullet)
                    score += 1
                except ValueError:
                    pass
                break


    win.fill(BLACK)
    pygame.draw.rect(win, rocket.color, (rocket.x, rocket.y, rocket.width, rocket.height))
    for bullet in rocket.bullets:
        pygame.draw.rect(win, RED, (bullet.x, bullet.y, 5, 10))
    for asteroid in asteroids:
        pygame.draw.circle(win, WHITE, (asteroid.x + asteroid.radius, asteroid.y + asteroid.radius), asteroid.radius)

    font = pygame.font.SysFont(None, 36)
    text = font.render(f"Score: {score}", True, WHITE)
    win.blit(text, (10, 10))

    pygame.display.flip()


ser.close()
pygame.quit()
