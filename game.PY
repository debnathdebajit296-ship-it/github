import pygame
import random

# Initialize pygame
pygame.init()

# Window setup
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stone, Paper & Scissors")

# Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Fonts
font = pygame.font.SysFont(None, 40)
large_font = pygame.font.SysFont(None, 60)

# Load images
rock_img = pygame.image.load("rock.PNG")
paper_img = pygame.image.load("paper.PNG")
scissor_img = pygame.image.load("scissor.PNG")

IMG_SIZE = (200, 200)
rock_img = pygame.transform.scale(rock_img, IMG_SIZE)
paper_img = pygame.transform.scale(paper_img, IMG_SIZE)
scissor_img = pygame.transform.scale(scissor_img, IMG_SIZE)

# Utility: Draw text
def draw_text(text, font, colour, x, y):
    img = font.render(text, True, colour)
    rect = img.get_rect(center=(x, y))
    window.blit(img, rect)

# Utility: Draw button (event-based click detection)
def draw_button(text, x, y, w, h, inactive_colour, active_colour, events):
    mouse = pygame.mouse.get_pos()
    action = False

    # Hover effect
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(window, active_colour, (x, y, w, h))
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                action = True
    else:
        pygame.draw.rect(window, inactive_colour, (x, y, w, h))

    # Always draw text
    text_surf = font.render(text, True, BLACK)
    text_rect = text_surf.get_rect(center=(x + w/2, y + h/2))
    window.blit(text_surf, text_rect)

    return action

# Game loop
def game_loop():
    player_choice = None
    computer_choice = None
    result = None
    player_score = 0
    computer_score = 0

    running = True
    while running:
        window.fill(WHITE)

        # Collect events for this frame
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        # If no round in progress → show choice buttons
        if player_choice is None:
            if draw_button("Rock", 50, 450, 200, 100, RED, (255, 100, 100), events):
                player_choice = "rock"
            elif draw_button("Paper", 300, 450, 200, 100, GREEN, (100, 255, 100), events):
                player_choice = "paper"
            elif draw_button("Scissor", 550, 450, 200, 100, BLUE, (100, 100, 255), events):
                player_choice = "scissor"

            # Once a choice is made → computer picks + decide result
            if player_choice:
                computer_choice = random.choice(["rock", "paper", "scissor"])
                if player_choice == computer_choice:
                    result = "It's a Tie!"
                elif (player_choice == "rock" and computer_choice == "scissor") or \
                     (player_choice == "paper" and computer_choice == "rock") or \
                     (player_choice == "scissor" and computer_choice == "paper"):
                    result = "You Win!"
                    player_score += 1
                else:
                    result = "Computer Wins!"
                    computer_score += 1

        # If round done → show results
        else:
            # Show player choice
            player_img = rock_img if player_choice == "rock" else paper_img if player_choice == "paper" else scissor_img
            comp_img = rock_img if computer_choice == "rock" else paper_img if computer_choice == "paper" else scissor_img

            player_rect = player_img.get_rect(center=(200, HEIGHT//2 - 50))
            comp_rect = comp_img.get_rect(center=(WIDTH - 200, HEIGHT//2 - 50))

            window.blit(player_img, player_rect)
            window.blit(comp_img, comp_rect)

            # Show result text
            draw_text(result, large_font, BLACK, WIDTH//2, 100)

            # Next round button
            if draw_button("Next Round", 300, 500, 200, 70, (200, 200, 200), (150, 150, 150), events):
                player_choice = None
                computer_choice = None
                result = None

        # Draw scores
        draw_text(f"Player: {player_score}", font, BLACK, 120, 40)
        draw_text(f"Computer: {computer_score}", font, BLACK, WIDTH - 150, 40)

        pygame.display.update()

    pygame.quit()

# Run game
game_loop()
