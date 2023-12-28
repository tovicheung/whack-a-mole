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

def load_small(path: str):
    return pygame.transform.scale(pygame.image.load(path), (80, 80))

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
        everything.add(self)

    def update(self):
        self.life -= 1
        if self.life <= 0:
            self.kill()

    def check_mouse(self, mouse: tuple[int, int]): ...

class Mole(Entity):
    image = load_small("mole_final.png")

    def check_mouse(self, mouse):
        if self.rect.collidepoint(mouse):
            global score
            score += 1
            # screen will be too messy ... uncomment at your own risk!
            # Cross(*self.rect.center, (0, 0, 255))
            self.kill()

    def update(self):
        super().update()
        if pygame.sprite.spritecollideany(self, foxes) is not None:
            Cross(*self.rect.center, (0, 0, 255))
            self.kill()

highlight_width = 10
highlight_duration = FPS / 2

class PowerUp(Entity):
    # image = pygame.transform.scale(pygame.image.load("powerup_time.png"), (80, 80))

    def __init__(self, image, onclick):
        self.image = image
        self.onclick = onclick
        super().__init__() # self.image is needed for __init__

        Cross(*self.rect.center, (255, 0, 0))

    def wupdate(self):
        super().update()
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
            self.onclick()
            self.kill()

def powerup_time():
    global timer
    timer += 3

def powerup_fox():
    Fox()
    Fox()
    Fox()
    Fox()

powerups = [
    (load_small("powerup_time.png"), powerup_time),
    (load_small("powerup_fox.png"), powerup_fox)
]

fox_images: list[pygame.surface.Surface] = []
for x in range(7):
    image = pygame.image.load(f"fox/{x}.png")
    fox_images.append(pygame.transform.scale(image, (image.get_width() // 3, image.get_height() // 3)))
# fox_images = [pygame.image.load(f"fox/{x}.png") for x in range(7)]

class Fox(pygame.sprite.Sprite):    
    def __init__(self):
        super().__init__()
        self.frame = 0
        self.x = 0
        self.y = random.randint(0, HEIGHT)

        foxes.add(self)
        everything.add(self)

        self.walk()

    def walk(self):
        self.frame += 1
        self.frame %= 7
        self.image = fox_images[self.frame]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.x += 20

        if self.x >= WIDTH:
            self.kill()

class Cross(pygame.sprite.Sprite):
    # cross effect
    width = 10

    def __init__(self, x, y, color):
        super().__init__()
        self.x = x
        self.y = y
        self.color = color
        self.image = pygame.surface.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.life = FPS / 2

        everything.add(self)

    def update(self):
        self.image.fill((0, 0, 0, 0))
        
        alpha = round(self.life / highlight_duration * 255)

        vline = pygame.Surface((self.width, HEIGHT), pygame.SRCALPHA)
        vline.fill((*self.color, alpha))
        self.image.blit(vline, (self.x - self.width / 2, 0))
        
        hline = pygame.Surface((WIDTH, self.width), pygame.SRCALPHA)
        hline.fill((*self.color, alpha))
        self.image.blit(hline, (0, self.y - self.width / 2))
        
        self.life -= 1
        if self.life <= 0:
            self.kill()


# Setup

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
buffer = pygame.surface.Surface((WIDTH, HEIGHT), pygame.SRCALPHA) # for the wobble effect

everything = pygame.sprite.Group() # everything that needs to be drawn
entities = pygame.sprite.Group() # interactive and updates per tick
foxes = pygame.sprite.Group() # separate as foxes aren't interactive

score = 0
timer = 20
wobble = 0 # how many ticks left to wobble
wobble_by = 3
wobble_for = FPS * 0.5

def gen_next_powerup():
    # Generate powerup in X to Y seconds
    return timer - random.randint(2, 5)

next_powerup = gen_next_powerup()

# Events

SPAWN_MOLE = pygame.USEREVENT + 1
TICK_1S = pygame.USEREVENT + 2
FOX_WALK = pygame.USEREVENT + 3

pygame.time.set_timer(SPAWN_MOLE, 300)
pygame.time.set_timer(TICK_1S, 1000)
pygame.time.set_timer(FOX_WALK, 50)

# Game loop

Mole() # no need to wait 1 second for first mole

# Fox()
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
        elif event.type == FOX_WALK:
            for fox in foxes:
                fox.walk()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for entity in entities:
                entity.check_mouse(event.pos)

    everything.update()
    pygame.sprite.Sprite.update
    everything.draw(buffer)

    if timer <= next_powerup:
        next_powerup = gen_next_powerup()
        PowerUp(*random.choice(powerups))
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
    buffer.fill((0, 0, 0, 0)) # clear the buffer

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
