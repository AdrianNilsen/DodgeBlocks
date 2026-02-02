import pygame, sys, random

pygame.init()

WIDTH, HEIGHT = 1280, 720
FONT = pygame.font.SysFont("Consolas", int(WIDTH/20))

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong!")
CLOCK = pygame.time.Clock()

#Klasser

class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(0, 0, 10, 100)
        self.rect.center = (x, y)

    def move_player(self, keys):
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.top -= 2
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.bottom += 2

    def move_ai(self, ball):
        if self.rect.y < ball.rect.y:
            self.rect.top += 1
        if self.rect.bottom > ball.rect.y:
            self.rect.bottom -= 1

    def draw(self, screen):
        pygame.draw.rect(screen, "white", self.rect)


class Ball:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 20, 20)
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.x_speed = 1
        self.y_speed = 1

    def reset(self):
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.x_speed = random.choice([1, -1])
        self.y_speed = random.choice([1, -1])

    def move(self):
        self.rect.x += self.x_speed * 2
        self.rect.y += self.y_speed * 2

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.rect.center, 10)

#Objekter 

player = Paddle(WIDTH - 100, HEIGHT / 2)
opponent = Paddle(100, HEIGHT / 2)
ball = Ball()
player_score, opponent_score = 0, 0

# Game loop

while True:
    keys_pressed = pygame.key.get_pressed()

    player.move_player(keys_pressed)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()




    # Ball kollisjon med veggene
    if ball.rect.y >= HEIGHT:
        ball.y_speed = -1
    if ball.rect.y <= 0:
        ball.y_speed = 1

    # Scoring
    if ball.rect.x <= 0:
        player_score += 1
        ball.reset()
      

    if ball.rect.x >= WIDTH:
        opponent_score += 1
        ball.reset()
          
   
    # Paddle kollisjon
    if player.rect.x - ball.rect.width <= ball.rect.x <= player.rect.right and \
       ball.rect.y in range(player.rect.top - ball.rect.width, player.rect.bottom + ball.rect.width):
        ball.x_speed = -1

    if opponent.rect.x - ball.rect.width <= ball.rect.x <= opponent.rect.right and \
       ball.rect.y in range(opponent.rect.top - ball.rect.width, opponent.rect.bottom + ball.rect.width):
        ball.x_speed = 1

    
    


   

    opponent.move_ai(ball)
    ball.move()

    # Draw
    SCREEN.fill("black")
    player.draw(SCREEN)
    opponent.draw(SCREEN)
    ball.draw(SCREEN)

    player_score_text = FONT.render(str(player_score), True, "white")
    opponent_score_text = FONT.render(str(opponent_score), True, "white")

    SCREEN.blit(player_score_text, (WIDTH/2+50, 50))
    SCREEN.blit(opponent_score_text, (WIDTH/2-50, 50))

    pygame.display.update()
    CLOCK.tick(300)
