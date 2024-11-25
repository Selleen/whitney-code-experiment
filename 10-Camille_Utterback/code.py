import random
import pygame
import sys

# Define constants
ScreenX = 800  # Screen width
ScreenY = 600  # Screen height
line_length = 100
num_rectangles = 10

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((ScreenX, ScreenY))
pygame.display.set_caption('dotodot')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create rectangles randomly
rectangles = []

def draw_random_rectangles():
    for _ in range(num_rectangles):
        x = random.randint(0, ScreenX - line_length)
        y = random.randint(0, ScreenY - line_length)
        width = random.randint(20, 100)
        height = random.randint(20, 100)
        rectangles.append(pygame.Rect(x, y, width, height))

def draw_rectangles():
    for rect in rectangles:
        pygame.draw.rect(screen, BLACK, rect, 2)

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            print(f"Mouse clicked at ({x}, {y})")

def main():
    draw_random_rectangles()
    while True:
        screen.fill(WHITE)
        handle_events()
        draw_rectangles()
        pygame.display.flip()

if __name__ == "__main__":
    main()
