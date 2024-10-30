import pygame
import random
import time
import csv
from datetime import datetime

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
        self.correctness = []  # To store whether the trial was correct or false

    def draw_circle(self, color):
        """Draws a larger central circle filled with the given color."""
        pygame.draw.circle(self.screen, color, (self.screen_width // 2, 250), 100)  # Adjusted y-position

    def draw_color_buttons(self, correct_color_name, target_color):
        """Draws larger, light-grey rectangles with color names, each in a unique color, with one correct option."""
        button_width = 200
        button_height = 100
        
        # Updated positions for two rows of two buttons, adjusted left and right
        button_positions = [
            (self.screen_width // 2 - button_width // 2 - 150, 400),  # Adjusted y-position
            (self.screen_width // 2 + button_width // 2 - 50, 400),   # Adjusted y-position
            (self.screen_width // 2 - button_width // 2 - 150, 575),  # Adjusted y-position
            (self.screen_width // 2 + button_width // 2 - 50, 575)    # Adjusted y-position
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
    
    def check_if_exists(self, participant_id, trial):
        """Check if the given id and trial already exists in the CSV file."""
        try:
            with open("reaction_times.csv", "r") as f:
                reader = csv.reader(f)
                header = next(reader)  # Read the header

                # Iterate over each row in the CSV
                for row in reader:
                    if row[0] == str(participant_id) and int(row[1]) == trial:
                        print(f"ID {participant_id} and Trial {trial} already exist.")  # Print statement
                        return True  # Found matching ID and trial
        except FileNotFoundError:
            return False  
        return False  # ID and trial do not exist    

    def save_reaction_times(self, reaction_times, correctness, participant_id, trial, group, gender, age, current_time):
        """Save reaction times and correctness to a CSV file, appending new data"""

        with open("reaction_times.csv", "a", newline='') as f:
            writer = csv.writer(f)
            # If the file is empty, write the header
            if f.tell() == 0:  
                tries = [i for i in range(1, 11)]
                # Adding correctness columns
                header = ["id", "trial", "gender", "age", "time"] + tries + ["correctness_" + str(i) for i in range(1, 11)]
                writer.writerow(header) 

            # Create a row with participant information and reaction times/correctness
            
            # Prepare the data for writing
            reaction_times = reaction_times + [None] * (10 - len(reaction_times))  # Fill the rest with None
            correctness = correctness + [None] * (10 - len(correctness))  # Fill the rest with None
            row = [participant_id, trial, gender, age, current_time]
            row.extend(reaction_times)
            row.extend(correctness)
            writer.writerow(row)

    def run_test(self, participant_id, trial, group, gender, age, current_time, practice=False):   
        running = True
        trial_count = 0  # Initialize trial count
        if practice:
            total_trials = 3
        else:
            total_trials = 10
        
        while running and trial_count < total_trials:
            self.screen.fill(WHITE)
            
            # Draw the title
            title_surface = self.font.render("Press the name of the color", True, BLACK)
            title_rect = title_surface.get_rect(center=(self.screen_width // 2, 100))  # Adjusted y-position for title
            self.screen.blit(title_surface, title_rect)

            # Pick a color for the central circle
            target_color_name = random.choice(self.color_names)
            target_color = self.colors[target_color_name]
            self.draw_circle(target_color)
            
            # Draw color buttons and store their properties
            buttons = self.draw_color_buttons(target_color_name, target_color)
            pygame.display.flip()
            
            # Start timing user response
            start_time = time.time()
            clicked = False
            
            while not clicked:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        clicked = True
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        correct_selection = False
                        for button_rect, color_name, font_color in buttons:
                            if button_rect.collidepoint(pos):
                                if color_name == target_color_name:
                                    reaction_time = time.time() - start_time
                                    self.reaction_times.append(reaction_time)
                                    self.correctness.append("Correct")  # Store correctness
                                else:
                                    self.reaction_times.append(time.time() - start_time)
                                    self.correctness.append("False")  # Store correctness

                                clicked = True  # Move to the next trial on any click
                                break
            
            trial_count += 1  # Increment trial count after each trial
            
            pygame.time.delay(500)  # Brief delay before next trial
            self.show_continue_message()  # Show continue message after any mouse click
            pygame.time.delay(500)

        # Save results at the end of the test
        if not practice:
            self.save_reaction_times(self.reaction_times, self.correctness, participant_id, trial, group, gender, age, current_time)
        pygame.quit()

    def show_continue_message(self):
        """Displays a message instructing the user to click to continue."""
        self.screen.fill(WHITE)
        message = "Click to continue to the next trial."
        text_surface = self.font.render(message, True, BLACK)
        text_rect = text_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False  # Exit the loop on mouse click

if __name__ == "__main__":
    test = StroopTest()
    practice = True
    gender = "M" 
    age = 29
    group = "control"  # "exercise" or "control"
    current_time = datetime.now().strftime("%H:%M:%S")
    participant_id = 1
    trial = 1

    if not test.check_if_exists(participant_id, trial):
        test.run_test(participant_id, trial, group, gender, age, current_time, practice)
