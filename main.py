import pygame 
import random 

# Constants

GRASS = (167, 255, 100) 
WIDTH = 800
HEIGHT = 800
FPS = 60

# Resources

pygame.font.init()
font = pygame.font.SysFont("Comic Sans MS", 20)
mole_image = pygame.transform.scale(pygame.image.load("mole_final.png"), (80, 80))

# Mole sprite

class Mole(pygame.sprite.Sprite):
    LIFETIME = 3 * FPS

    def __init__(self): 
        super().__init__()
        self.image = mole_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)

        self.life = type(self).LIFETIME

        moles.add(self)

    def tick(self):
        self.life -= 1
        if self.life <= 0:
            self.kill()

    def check_mouse(self, mouse):
        if self.rect.collidepoint(mouse):
            global score
            score += 1
            self.kill()

# Setup

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

moles = pygame.sprite.Group()

score = 0
timer = 10

# Events

SPAWN_MOLE = pygame.USEREVENT + 1
TICK_1S = pygame.USEREVENT + 2

pygame.time.set_timer(SPAWN_MOLE, 300)
pygame.time.set_timer(TICK_1S, 1000)

# Game loop

Mole() # no need to wait 1 second for first mole

running = True
while running: 
    screen.fill(GRASS)

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            # Don't show end screen, immediate stop program
            pygame.quit()
            exit()
        elif event.type == SPAWN_MOLE:
            Mole()
        elif event.type == TICK_1S:
            timer -= 1
            if timer <= 0:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for mole in moles:
                mole.check_mouse(event.pos)

    for mole in moles:
        mole.tick()

    moles.update() 
    moles.draw(screen)
    
    screen.blit(font.render(f"Score: {score} | Time: {timer}s", False, (0, 0, 0)), (0, 0))
    pygame.draw.circle(screen, (255, 0, 0), pygame.mouse.get_pos(), radius=10) # helpful (?) dot

    pygame.display.flip() 
    clock.tick(FPS)

text = font.render(f"Time's up! Your score: {score}", False, (0, 0, 0), (255, 255, 255))
screen.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
pygame.display.flip()

# freeze end screen

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
