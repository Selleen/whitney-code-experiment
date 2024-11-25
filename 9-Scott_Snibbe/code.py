import pygame
import math
import sys

WIDTH, HEIGHT = 800, 800
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

DAMPING = 0.97
GRAVITY = 0.005
MAGNETISM = 0.1
HEIGHT_FACTOR = 0.1
MASS = 1.0
TIME_STEP = 0.01

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulación Tripolar")
clock = pygame.time.Clock()

center_x, center_y = WIDTH // 2, HEIGHT // 2
scale = min(center_x, center_y)

magnets = []
for i in range(3):
    angle = math.pi / 2 + (2 * math.pi / 3) * i
    magnets.append((0.5 * math.cos(angle), 0.5 * math.sin(angle)))


def draw_line(x1, y1, x2, y2):
    """Draw a line between two points scaled to the screen space."""
    pygame.draw.line(
        screen, BLACK,
        (int(x1 * scale + center_x), int(y1 * scale + center_y)),
        (int(x2 * scale + center_x), int(y2 * scale + center_y)),
        1
    )


def update_paths(x, y):
    """Simulate the pendulum's trajectories and draw them."""
    vx, vy = 0, 0
    filt_vel = 1
    iterations = 0

    while filt_vel > 0.1 and iterations < 10000:
        iterations += 1

        fx, fy = 0, 0
        r = x ** 2 + y ** 2
        r = max(r, 0.00001) 
        fx -= (x * GRAVITY) / r
        fy -= (y * GRAVITY) / r

        for mx, my in magnets:
            dx = mx - x
            dy = my - y
            dist = math.sqrt(dx ** 2 + dy ** 2 + HEIGHT_FACTOR ** 2)
            dist = max(dist, 0.00001)
            force = MAGNETISM / (dist ** 3)
            fx += force * dx
            fy += force * dy

        fx -= vx * DAMPING
        fy -= vy * DAMPING

        vx += TIME_STEP * fx / MASS
        vy += TIME_STEP * fy / MASS

        filt_vel = 0.99 * filt_vel + 0.1 * max(abs(vx), abs(vy))

        next_x = x + vx
        next_y = y + vy

        draw_line(x, y, next_x, next_y)

        x, y = next_x, next_y


mouse_pressed = False
probe_x, probe_y = None, None

running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pressed = True
            probe_x, probe_y = None, None
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_pressed = False
        elif event.type == pygame.MOUSEMOTION and mouse_pressed:
            mouse_x, mouse_y = event.pos
            probe_x = (mouse_x - center_x) / scale
            probe_y = (mouse_y - center_y) / scale

    if probe_x is not None and probe_y is not None:
        update_paths(probe_x, probe_y)

    for mx, my in magnets:
        screen_x = int(mx * scale + center_x)
        screen_y = int(my * scale + center_y)
        pygame.draw.circle(screen, BLACK, (screen_x, screen_y), 5)

    pygame.display.flip()
    clock.tick(FPS)

# Exit Pygame
pygame.quit()
sys.exit()
