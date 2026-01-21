import pygame
import random
import sys

# --------------------
# INITIALISERING
# --------------------
pygame.init()

WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge the Blocks")

CLOCK = pygame.time.Clock()
FONT = pygame.font.SysFont(None, 40)

# Farger
WHITE = (255, 255, 255)
RED = (200, 50, 50)
BLUE = (50, 100, 255)
BLACK = (0, 0, 0)

# --------------------
# KLASSER
# --------------------
class Player:
    """Spilleren som styres av brukeren"""
    def __init__(self):
        self.width = 60
        self.height = 20
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - 60
        self.speed = 6
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def draw(self):
        pygame.draw.rect(SCREEN, BLUE, self.rect)


class Block:
    """Fallende blokk som spilleren må unngå"""
    def __init__(self, speed):
        self.size = 40
        self.x = random.randint(0, WIDTH - self.size)
        self.y = -self.size
        self.speed = speed
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def update(self):
        self.rect.y += self.speed

    def draw(self):
        pygame.draw.rect(SCREEN, RED, self.rect)


# --------------------
# FUNKSJONER
# --------------------
def draw_text(text, x, y, color=WHITE):
    img = FONT.render(text, True, color)
    SCREEN.blit(img, (x, y))


def start_screen():
    while True:
        SCREEN.fill(BLACK)
        draw_text("DODGE THE BLOCKS", 260, 200)
        draw_text("Trykk SPACE for å starte", 240, 260)
        draw_text("Bruk piltaster for å bevege deg", 200, 320)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return


def game_over_screen(score):
    while True:
        SCREEN.fill(BLACK)
        draw_text("GAME OVER", 330, 200, RED)
        draw_text(f"Poeng: {score}", 340, 260)
        draw_text("Trykk SPACE for å spille igjen", 210, 320)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return


# --------------------
# HOVEDSPILL
# --------------------
def main():
    start_screen()

    player = Player()
    blocks = []
    score = 0
    block_timer = 0
    block_speed = 4

    running = True
    while running:
        CLOCK.tick(60)
        SCREEN.fill(BLACK)

        # ---- Events ----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # ---- Input ----
        keys = pygame.key.get_pressed()
        player.move(keys)

        # ---- Blokker ----
        block_timer += 1
        if block_timer > 40:
            blocks.append(Block(block_speed))
            block_timer = 0

        for block in blocks:
            block.update()
            block.draw()

            # Kollisjon
            if block.rect.colliderect(player.rect):
                game_over_screen(score)
                return main()

        # Fjern blokker som er ute av skjermen
        blocks = [b for b in blocks if b.rect.top < HEIGHT]

        # ---- Vanskelighetsgrad ----
        score += 1
        if score % 300 == 0:
            block_speed += 1

        # ---- Tegning ----
        player.draw()
        draw_text(f"Poeng: {score}", 10, 10)

        pygame.display.update()


# --------------------
# START PROGRAM
# --------------------
main()
