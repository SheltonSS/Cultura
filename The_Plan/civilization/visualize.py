import pygame
import random
from civilization import Civilization

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600  # Window size
GRID_SIZE = 20  # Size of each grid cell
FPS = 30  # Frames per second
BACKGROUND_COLOR = (34, 139, 34)  # Green for the map background

# Colors
CIVILIZATION_COLOR = (255, 215, 0)  # Gold for civilizations
EVENT_COLOR = (255, 69, 0)  # Red for events
TEXT_COLOR = (255, 255, 255)  # White for text

# Initialize Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Civilization Simulation")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.Font(None, 24)

# Helper functions
def draw_grid():
    """Draw the grid on the screen."""
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, (200, 200, 200), (x, 0), (x, HEIGHT))  # Vertical lines
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, (200, 200, 200), (0, y), (WIDTH, y))  # Horizontal lines

def draw_civilizations(civilizations):
    """Draw civilizations on the map."""
    for civ in civilizations:
        x, y = civ.location
        pygame.draw.circle(
            screen,
            CIVILIZATION_COLOR,
            (x * GRID_SIZE + GRID_SIZE // 2, y * GRID_SIZE + GRID_SIZE // 2),
            GRID_SIZE // 3,
        )
        # Draw civilization name
        text = font.render(civ.name, True, TEXT_COLOR)
        screen.blit(text, (x * GRID_SIZE + 5, y * GRID_SIZE - 10))


# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw everything
    screen.fill(BACKGROUND_COLOR)
    draw_grid()
    # draw_civilizations(civilizations)
    # draw_events(events)

    # Update the display
    pygame.display.flip()
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
