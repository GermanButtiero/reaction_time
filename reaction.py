import pygame
import random
import time
import sys

# Initialize pygame
pygame.init()

# Set window
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Reaction Time Test")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Font settings
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

def draw_text(text, font, color, x, y):
    """Render text on screen"""
    screen_text = font.render(text, True, color)
    screen.blit(screen_text, [x, y])

def reaction_time_test():
    """Main logic for the reaction time test"""
    running = True
    waiting_for_reaction = False
    waiting_for_go = False
    reaction_start_time = 0
    reaction_time = 0
    trial_count = 0
    reaction_times = []
    too_soon = False  # To handle premature key presses

    while running:
        screen.fill(WHITE)
        draw_text("Press space to start", font, BLACK, 100, 150)
        draw_text("Reopen the game to reset", small_font, BLACK, 150, 300)
        pygame.display.flip()

        # Wait for user input
        while not waiting_for_go and not waiting_for_reaction and running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not waiting_for_go and not waiting_for_reaction:
                        # Display "Wait..." in black
                        screen.fill(BLACK)
                        draw_text("Wait...", font, WHITE, 200, 150)
                        pygame.display.flip()

                        # Start random delay before showing "GO!"
                        random_delay = random.uniform(2, 5)
                        go_time = time.time() + random_delay
                        waiting_for_go = True

        # During random delay, check for premature key press
        while waiting_for_go and not waiting_for_reaction:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if time.time() < go_time:  # Pressed too soon
                            too_soon = True
                            waiting_for_go = False
                            # Display "Too Soon!" and return to the start
                            screen.fill(WHITE)
                            draw_text("Too Soon!", font, RED, 150, 150)
                            pygame.display.flip()
                            pygame.time.delay(2000)
                            break

            # If the random delay has passed, show "GO!"
            if time.time() >= go_time:
                screen.fill(GREEN)
                draw_text("GO!", font, RED, 250, 150)
                pygame.display.flip()
                reaction_start_time = time.time()  # Start the timer for reaction time
                waiting_for_reaction = True
                waiting_for_go = False

        # Wait for user's response after "GO!" appears
        while waiting_for_reaction and running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        reaction_time = time.time() - reaction_start_time
                        trial_count += 1
                        reaction_times.append(reaction_time)

                        # Display the reaction time for 3 seconds
                        screen.fill(WHITE)
                        draw_text(f"Reaction: {reaction_time:.3f} s", small_font, RED, 150, 150)
                        draw_text(f"Trial: {trial_count}", small_font, BLACK, 150, 200)
                        pygame.display.flip()
                        pygame.time.delay(3000)  # Display the result for 3 seconds
                        waiting_for_reaction = False  # Reset the test

        pygame.display.update()

    # Print collected data when the test is closed
    pygame.quit()
    print("Test finished. Reaction times (in seconds):")
    for i, rt in enumerate(reaction_times, 1):
        print(f"Trial {i}: {rt:.3f} seconds")
 

# Run the reaction time test
reaction_time_test()
