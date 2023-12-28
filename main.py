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

# Mole sprite

class Entity(pygame.sprite.Sprite):
    # Common behaviour between moles and powerups

    # Constants
    lifetime = 3 * FPS
    image: pygame.surface.Surface

    def __init__(self): 
        super().__init__()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)

        self.life = type(self).lifetime

        entities.add(self)

    def tick(self):
        self.life -= 1
        if self.life <= 0:
            self.kill()

    def check_mouse(self, mouse: tuple[int, int]): ...

class Mole(Entity):
    image = pygame.transform.scale(pygame.image.load("mole_final.png"), (80, 80))

    def check_mouse(self, mouse):
        if self.rect.collidepoint(mouse):
            global score
            score += 1
            self.kill()

highlight_width = 10
highlight_duration = FPS / 2
class PowerUp(Entity):
    image = pygame.transform.scale(pygame.image.load("powerup_time.png"), (80, 80))

    def tick(self):
        super().tick()
        age = self.lifetime - self.life
        if age < highlight_duration: # highlight exists for 0.5s

            # Sadly lines don't support transparency
            # pygame.draw.line(screen, pygame.color.Color(255, 0, 0, round(age / FPS * 255)), (0, self.rect.y), (WIDTH, self.rect.y), 10)
            # pygame.draw.line(screen, pygame.color.Color(255, 0, 0, round(age / FPS * 255)), (self.rect.x, 0), (self.rect.x, HEIGHT), 10)

            alpha = round(255 - age / highlight_duration * 255)

            vline = pygame.Surface((highlight_width, HEIGHT), pygame.SRCALPHA)
            vline.fill((255, 0, 0, alpha))
            buffer.blit(vline, (self.rect.centerx - highlight_width / 2, 0))
            
            hline = pygame.Surface((WIDTH, highlight_width), pygame.SRCALPHA)
            hline.fill((255, 0, 0, alpha))
            buffer.blit(hline, (0, self.rect.centery - highlight_width / 2))


    def check_mouse(self, mouse):
        if self.rect.collidepoint(mouse):
            global timer
            timer += 3
            self.kill()

# Setup

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
buffer = pygame.surface.Surface((WIDTH, HEIGHT), pygame.SRCALPHA) # for the wobble effect

entities = pygame.sprite.Group()

score = 0
timer = 10
wobble = 0 # how many ticks left to wobble
wobble_by = 3
wobble_for = FPS * 0.5

def gen_next_powerup():
    # Generate powerup in X to Y seconds
    return timer - random.randint(2, 3)

next_powerup = gen_next_powerup()

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
            for entity in entities:
                entity.check_mouse(event.pos)

    for entity in entities:
        entity.tick()

    entities.update() 
    entities.draw(buffer)

    if timer <= next_powerup:
        next_powerup = gen_next_powerup()
        PowerUp()
        wobble += wobble_for
        
    pygame.draw.circle(buffer, (255, 0, 0), pygame.mouse.get_pos(), radius=10) # helpful (?) dot

    if wobble:
        wobble -= 1
        screen.blit(buffer, (random.randint(-wobble_by, wobble_by), random.randint(-wobble_by, wobble_by)))
    else:
        screen.blit(buffer, (0, 0))

    # Text above everything else
    screen.blit(font.render(f"Score: {score} | Time: {timer}s", False, (0, 0, 0)), (0, 0))

    pygame.display.flip()
    buffer.fill((0, 0, 0, 0))

    clock.tick(FPS)

# end screen

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
