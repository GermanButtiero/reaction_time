import pygame
import random
import time

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GREY = (150, 150, 150)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)

class StroopTest:
    def __init__(self):
        pygame.init()
        self.font = pygame.font.Font(None, 60)
        self.screen_width = 1500
        self.screen_height = 800
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Stroop Test")

        # Mapping color names to their RGB values
        self.colors = {
            "RED": RED,
            "GREEN": GREEN,
            "BLUE": BLUE,
            "YELLOW": YELLOW,
            "PURPLE": PURPLE,
            "ORANGE": ORANGE
        }
        self.color_names = list(self.colors.keys())  # List of color names
        self.reaction_times = []

    def draw_circle(self, color):
        """Draws a larger central circle filled with the given color."""
        pygame.draw.circle(self.screen, color, (self.screen_width // 2, 150), 100)  # Increased circle radius to 100

    def draw_color_buttons(self, correct_color_name, target_color):
        """Draws larger, light-grey rectangles with color names, each in a unique color, with one correct option."""
        button_width = 200
        button_height = 100
        
        # Updated positions for two rows of two buttons, adjusted left and right
        button_positions = [
        (self.screen_width // 2 - button_width // 2 - 150, 300),  # Adjusted Top left
        (self.screen_width // 2 + button_width // 2 - 50, 300),   # Adjusted Top right (moved closer to center)
        (self.screen_width // 2 - button_width // 2 - 150, 475),  # Adjusted Bottom left
        (self.screen_width // 2 + button_width // 2 - 50, 475)    # Adjusted Bottom right (moved closer to center)
    ]

        
        buttons = []
        
        # Ensure the correct color name is in the list of options
        incorrect_options = [name for name in self.color_names if name != correct_color_name]
        options = random.sample(incorrect_options, 3) + [correct_color_name]
        random.shuffle(options)  # Shuffle to randomize the position of the correct option
        
        # Exclude the target color from font colors
        available_colors = list(self.colors.values())
        available_colors.remove(target_color)  # Remove the circle color from font color options
        font_colors = random.sample(available_colors, len(options))

        for position, color_name, font_color in zip(button_positions, options, font_colors):
            button_rect = pygame.Rect(position[0], position[1], button_width, button_height)  # Button dimensions
            buttons.append((button_rect, color_name, font_color))
            
            # Draw the rectangle button with light grey fill
            pygame.draw.rect(self.screen, LIGHT_GREY, button_rect)
            pygame.draw.rect(self.screen, BLACK, button_rect, 3)  # Black border for button
            
            # Render the color name inside the rectangle
            text_surface = self.font.render(color_name, True, font_color)
            text_rect = text_surface.get_rect(center=button_rect.center)
            self.screen.blit(text_surface, text_rect)
        
        return buttons

    def run_test(self):
        running = True
        while running:
            self.screen.fill(WHITE)
            
            # Pick a color for the central circle
            target_color_name = random.choice(self.color_names)
            target_color = self.colors[target_color_name]
            self.draw_circle(target_color)
            
            # Draw color buttons and store their properties
            buttons = self.draw_color_buttons(target_color_name, target_color)
            pygame.display.flip()
            
            # Start timing user response
            start_time = time.time()
            correct_selection = False
            
            while not correct_selection:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        correct_selection = True
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        for button_rect, color_name, font_color in buttons:
                            if button_rect.collidepoint(pos):
                                if color_name == target_color_name:
                                    reaction_time = time.time() - start_time
                                    self.reaction_times.append(reaction_time)
                                    print(f"Correct! Reaction Time: {reaction_time:.3f} seconds")
                                    correct_selection = True  # Proceed only if the correct choice is made
                                else:
                                    print("Incorrect selection. Try again.")
            
            pygame.time.delay(1000)  # Brief delay before next trial

        pygame.quit()

if __name__ == "__main__":
    test = StroopTest()
    test.run_test()
