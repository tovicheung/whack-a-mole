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

def load_small(path: str, scale=(80, 80)):
    return pygame.transform.scale(pygame.image.load(path), scale)

def load_shrink(path: str, by: int):
    image = pygame.image.load(path)
    return pygame.transform.scale(image, (image.get_width() // by, image.get_height() // by))

# Sprites

class Entity(pygame.sprite.Sprite):
    # Common behaviour between moles and powerups

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
    image = load_small("assets/mole.png")

    def die(self):
        global score
        score += 1
        self.kill()

    def check_mouse(self, mouse):
        if self.rect.collidepoint(mouse) or self.rect.colliderect(hammer.rect):
            # screen will be too messy ... uncomment at your own risk!
            # Cross(*self.rect.center, (0, 0, 255))
            self.die()

    def update(self):
        super().update()

        if pygame.sprite.spritecollideany(self, foxes) is not None:
            Cross(*self.rect.center, "#ff6d00")
            self.die()

        if pygame.sprite.spritecollideany(self, winds) is not None:
            Cross(*self.rect.center, "#64b0de")
            self.die()

class PowerUp(Entity):
    def __init__(self, image, onclick):
        self.image = image
        self.onclick = onclick
        super().__init__() # self.image is needed for __init__

        Cross(*self.rect.center, (255, 0, 0))

    def check_mouse(self, mouse):
        if self.rect.collidepoint(mouse):
            self.onclick()
            self.kill()

def powerup_time():
    global timer
    timer += 5
    BlinkLine(BlinkLine.width // 2, "#f2c30a")

def powerup_fox():
    Fox()
    Fox()
    Fox()
    Fox()
    Fox()

def powerup_wind():
    Wind()

powerups = [
    (load_small("assets/powerup_time.png"), powerup_time),
    (load_small("assets/powerup_fox.png"), powerup_fox),
    (load_small("assets/powerup_wind.png"), powerup_wind)
]

fox_images: list[pygame.surface.Surface] = []
for x in range(7):
    image = pygame.image.load(f"assets/fox/{x}.png")
    fox_images.append(pygame.transform.scale(image, (image.get_width() // 3, image.get_height() // 3)))

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

class Wind(pygame.sprite.Sprite):
    image_original = load_small("assets/powerup_wind.png", (150, 150))
    lifetime = FPS * 3
    turn_by = -30

    def __init__(self):
        super().__init__()
        self.image = self.image_original
        self.rect = self.image.get_rect()
        self.angle = 0
        self.life = self.lifetime

        everything.add(self)
        winds.add(self)

    def update(self):
        self.angle += self.turn_by
        self.angle %= 360
        self.image = pygame.transform.rotate(self.image_original, self.angle)
        self.rect = self.image.get_rect()
        
        x, y = pygame.mouse.get_pos()
        self.rect.centerx = x
        self.rect.centery = y
        
        self.life -= 1
        if self.life <= 0:
            self.kill()

class Cross(pygame.sprite.Sprite):
    # cross effect
    width = 10
    lifetime = FPS / 2

    def __init__(self, x, y, color):
        super().__init__()
        self.x = x
        self.y = y
        self.color = pygame.Color(color)
        self.image = pygame.surface.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.life = FPS // 2

        everything.add(self)

    def update(self):
        self.image.fill((0, 0, 0, 0))
        
        alpha = round(self.life / self.lifetime * 255)
        self.color.a = alpha

        vline = pygame.Surface((self.width, HEIGHT), pygame.SRCALPHA)
        vline.fill(self.color)
        self.image.blit(vline, (self.x - self.width / 2, 0))
        
        hline = pygame.Surface((WIDTH, self.width), pygame.SRCALPHA)
        hline.fill(self.color)
        self.image.blit(hline, (0, self.y - self.width / 2))
        
        self.life -= 1
        if self.life <= 0:
            self.kill()

class BlinkLine(pygame.sprite.Sprite):
    width = 30
    lifetime = FPS

    def __init__(self, y, color):
        super().__init__()
        self.y = y
        self.color = pygame.Color(color)
        self.image = pygame.surface.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.life = self.lifetime

        everything.add(self)

    def update(self):
        self.image.fill((0, 0, 0, 0))

        self.color.a = round(self.life % 6 / 6) * 255
        hline = pygame.Surface((WIDTH, self.width), pygame.SRCALPHA)
        hline.fill(self.color)
        self.image.blit(hline, (0, self.y - self.width / 2))

        self.life -= 1
        if self.life <= 0:
            self.kill()

class Hammer(pygame.sprite.Sprite):
    image_original = load_shrink("assets/hammer.png", 7)

    def __init__(self):
        super().__init__()
        self.image = self.image_original
        self.rect = self.image.get_rect()
        self.state = 0
        # 0-1: normal
        # 2-3: rotating back to normal
        # 4-5: whack (rotate max)
        # 6-7: rotating to whack

        # everything.add(self) do not draw on buffer

    def update(self):
        if self.state in (2, 3, 6, 7):
            self.image = pygame.transform.rotate(self.image_original, 45)
        elif self.state in (4, 5):
            self.image = pygame.transform.rotate(self.image_original, 90)
        else:
            self.image = self.image_original

        x, y = pygame.mouse.get_pos()
        self.rect.centerx = x
        self.rect.centery = y

        if self.state > 0:
            self.state -= 1

        screen.blit(self.image, self.rect)


# Setup

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
buffer = pygame.surface.Surface((WIDTH, HEIGHT), pygame.SRCALPHA) # for the wobble effect

everything = pygame.sprite.Group() # everything that needs to be drawn
entities = pygame.sprite.Group() # interactive and updates per tick
foxes = pygame.sprite.Group()
winds = pygame.sprite.Group()

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

hammer = Hammer()
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
        elif event.type == FOX_WALK:
            for fox in foxes:
                fox.walk()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            hammer.state = 7
            for entity in entities:
                entity.check_mouse(event.pos)

    everything.update()
    everything.draw(buffer)

    if timer <= next_powerup:
        next_powerup = gen_next_powerup()
        PowerUp(*random.choice(powerups))
        wobble += wobble_for
    
    # cursor indicator (replaced by hammer)
    # pygame.draw.circle(buffer, (255, 0, 0), pygame.mouse.get_pos(), radius=10)

    if wobble:
        wobble -= 1
        screen.blit(buffer, (random.randint(-wobble_by, wobble_by), random.randint(-wobble_by, wobble_by)))
    else:
        screen.blit(buffer, (0, 0))
    
    hammer.update()

    # Text not affected by wobble
    screen.blit(font.render(f"Score: {score} | Time: {timer}s", False, (0, 0, 0)), (0, 0))

    # Alternative display, unused
    # timer_text = font.render(f"Time: {timer}s", False, (0, 0, 0))
    # timer_rect = timer_text.get_rect()
    # timer_rect.y = 0
    # timer_rect.x = WIDTH - timer_rect.width - 10
    # screen.blit(timer_text, timer_rect)

    pygame.display.flip()
    buffer.fill((0, 0, 0, 0)) # clear the buffer

    clock.tick(FPS)

# End screen

text = font.render(f"Time's up! Your score: {score}", False, (0, 0, 0), (255, 255, 255))
screen.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
pygame.display.flip()

# Freeze end screen

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
