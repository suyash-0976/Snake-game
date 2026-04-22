import pygame
import sys
import random
import os

pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20
FPS = 10
clock=pygame.time.Clock()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("softronix snake game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0) 

#font
font = pygame.font.SysFont("Arial", 24)

# High Score file
HIGHSCORE_FILE = "highscore.txt"

def get_high_score():
    if not os.path.exists(HIGHSCORE_FILE):
        return 0
    try:
        with open(HIGHSCORE_FILE, "r") as f:
            return int(f.read())
    except:
        return 0

def save_high_score(score):
    high_score = get_high_score()
    if score > high_score:
        with open(HIGHSCORE_FILE, "w") as f:
            f.write(str(score))

# Snake
class Snake:
    def __init__(self):  
        self.body = [(300, 300)]
        self.direction = (0, -GRID_SIZE)  # initial direction
        self.grow = False

    def draw(self):
        for segment in self.body:   
            pygame.draw.rect(screen, GREEN, (*segment, GRID_SIZE, GRID_SIZE))

    def change_direction(self,dx,dy):
     if(dx,dy)!=(-self.direction[0],-self.direction[1]):
         self.direction=(dx,dy)
    
    def move(self):
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        self.body.insert(0, new_head)

        if self.grow:
             self.grow = False
        else:
            self.body.pop()  # remove tail

    def check_collision(self):
        head = self.body[0]
        # Check wall collision
        if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
            return True
        # Check self collision
        if head in self.body[1:]: #[(300, 300),(300,280),(300,260)(300,300)]
            return True
        return False

#food
class Food:
    def __init__(self):
        self.position=self.random_position()
    def random_position(self):
        return(
            random.randrange(0, WIDTH, GRID_SIZE),
            random.randrange(0, HEIGHT, GRID_SIZE)
        )
    def draw(self): pygame.draw.rect(screen, RED, (*self.position, GRID_SIZE, GRID_SIZE))
    
# draw 

def draw_text(text, x, y, center=False):
    img = font.render(text, True, WHITE)
    if center:
        rect = img.get_rect(center=(x, y))
        screen.blit(img, rect)
    else:
        screen.blit(img, (x, y))

def game():
    running = True
    game_over = False
    score=0
    speed=FPS
    high_score = get_high_score()

    snake=Snake()
    food=Food()

    clock = pygame.time.Clock()

    # game loop
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if not game_over:
                    if event.key == pygame.K_UP:
                        snake.change_direction(0,-GRID_SIZE)

                    if event.key == pygame.K_DOWN:
                        
                        snake.change_direction(0,GRID_SIZE)
                    
                    if event.key == pygame.K_RIGHT:
                       snake.change_direction(GRID_SIZE,0)
                    
                    if event.key == pygame.K_LEFT:
                        snake.change_direction(-GRID_SIZE,0)

                if event.key == pygame.K_r and game_over:
                    return game()

        if not game_over:
            snake.move()

            # Food collision
            if snake.body[0] == food.position:
                snake.grow = True
                food.position = food.random_position()
                score+=10
                speed+=0.5
                
                # Collision check
            if snake.check_collision():
                game_over = True
                save_high_score(score)

                
        snake.draw()
        food.draw()

        if not game_over:
            draw_text(f"Score: {score}", 10, 10)
            draw_text(f"High Score: {high_score}", WIDTH - 150, 10)
        else:
            draw_text("Game Over! Press R to restart", WIDTH // 2, HEIGHT // 2 - 20, center=True)
            draw_text(f"Score: {score}  High Score: {max(score, high_score)}", WIDTH // 2, HEIGHT // 2 + 20, center=True)

        pygame.display.update()
        clock.tick(int(speed))


if __name__ == "__main__":
    game()