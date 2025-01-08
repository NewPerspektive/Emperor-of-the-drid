import pygame
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
HIGHLIGHT = (50, 150, 50)

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess-like Board Game")

# Define font
FONT = pygame.font.SysFont("Arial", 24)

# Figures
class Figure:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.selected = False

    def move(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            self.color,
            (self.x * SQUARE_SIZE + SQUARE_SIZE // 2, self.y * SQUARE_SIZE + SQUARE_SIZE // 2),
            SQUARE_SIZE // 3
        )

    def get_position(self):
        return self.x, self.y

# Functions to handle game logic
def draw_board():
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if (row + col) % 2 == 0 else GRAY
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def highlight_square(x, y):
    pygame.draw.rect(
        screen,
        HIGHLIGHT,
        (x * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
    )

def get_closest_square(mouse_x, mouse_y):
    grid_x = mouse_x // SQUARE_SIZE
    grid_y = mouse_y // SQUARE_SIZE
    return grid_x, grid_y

def is_valid_move(fig, target_x, target_y):
    dx = abs(fig.x - target_x)
    dy = abs(fig.y - target_y)
    return dx <= 1 and dy <= 1

# Game setup
running = True
turn = "player"
figures = [
    Figure(4, 4, BLACK),  # Player's figure (King or Warlord)
    Figure(2, 2, (255, 0, 0)),  # Opponent's figure
]
selected_figure = None

# Game loop
while running:
    screen.fill(WHITE)
    draw_board()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            grid_x, grid_y = get_closest_square(mouse_x, mouse_y)

            for fig in figures:
                if fig.get_position() == (grid_x, grid_y) and turn == "player":
                    selected_figure = fig

        if event.type == pygame.MOUSEBUTTONUP and selected_figure:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            grid_x, grid_y = get_closest_square(mouse_x, mouse_y)

            if is_valid_move(selected_figure, grid_x, grid_y):
                selected_figure.move(grid_x, grid_y)
                turn = "opponent" if turn == "player" else "player"

            selected_figure = None

    # Highlight valid moves if a figure is selected
    if selected_figure:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        grid_x, grid_y = get_closest_square(mouse_x, mouse_y)

        if is_valid_move(selected_figure, grid_x, grid_y):
            highlight_square(grid_x, grid_y)

    # Draw figures
    for fig in figures:
        fig.draw(screen)

    # Display turn
    turn_text = FONT.render(f"Turn: {turn.capitalize()}", True, BLACK)
    screen.blit(turn_text, (10, 10))

    pygame.display.flip()

pygame.quit()

