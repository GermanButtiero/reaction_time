import pygame
import random
import time
import csv
from datetime import datetime

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
LIGHT_GREY = (200, 200, 200)

class StroopTest:
    def __init__(self):
        pygame.init()
        self.font = pygame.font.Font(None, 60)
        self.screen_width = 1500
        self.screen_height = 800
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Stroop Test")

        self.colors = {
            "RED": RED,
            "GREEN": GREEN,
            "BLUE": BLUE,
            "YELLOW": YELLOW,
            "PURPLE": PURPLE,
            "ORANGE": ORANGE
        }
        self.color_names = list(self.colors.keys())
        self.reaction_times = []
        self.correctness = []
        self.trial_types = []

    def draw_color_word(self, target_color_name, ink_color):
        """Draws the target color name in the given ink color at the top center."""
        large_font = pygame.font.Font(None, 100)
        text_surface = large_font.render(target_color_name, True, ink_color)
        text_rect = text_surface.get_rect(center=(self.screen_width // 2, 250))
        self.screen.blit(text_surface, text_rect)

    def draw_color_buttons(self, target_ink_color_name):
        """Draws four buttons with color names, all in black ink, and ensures target ink color is among the options."""
        button_width = 200
        button_height = 100
        button_positions = [
            (self.screen_width // 2 - button_width // 2 - 150, 400),
            (self.screen_width // 2 + button_width // 2 - 50, 400),
            (self.screen_width // 2 - button_width // 2 - 150, 575),
            (self.screen_width // 2 + button_width // 2 - 50, 575)
        ]

        buttons = []
        
        # Ensure the target ink color name is included among the options
        incorrect_options = [name for name in self.color_names if name != target_ink_color_name]
        options = random.sample(incorrect_options, 3) + [target_ink_color_name]
        random.shuffle(options)  # Shuffle to randomize the position of the correct answer

        for position, color_name in zip(button_positions, options):
            button_rect = pygame.Rect(position[0], position[1], button_width, button_height)
            buttons.append((button_rect, color_name))

            pygame.draw.rect(self.screen, LIGHT_GREY, button_rect)
            pygame.draw.rect(self.screen, BLACK, button_rect, 3)

            text_surface = self.font.render(color_name, True, BLACK)
            text_rect = text_surface.get_rect(center=button_rect.center)
            self.screen.blit(text_surface, text_rect)

        return buttons

    def check_if_exists(self, participant_id, trial):
        """Check if the given ID and trial already exists in the CSV file."""
        try:
            with open("reaction_times.csv", "r") as f:
                reader = csv.reader(f)
                header = next(reader)

                for row in reader:
                    if row[0] == str(participant_id) and int(row[1]) == trial:
                        print(f"ID {participant_id} and Trial {trial} already exist.")
                        return True
        except FileNotFoundError:
            return False
        return False

    def save_reaction_times(self, participant_id, trial, group, gender, age, current_time):
        """Save reaction times and correctness to a CSV file, appending new data."""
        with open("reaction_times.csv", "a", newline='') as f:
            writer = csv.writer(f)
            if f.tell() == 0:
                header = ["id", "trial", "gender", "group", "age", "time", "trial_type"] + \
                         ["reaction_time_" + str(i+1) for i in range(10)] + \
                         ["correctness_" + str(i+1) for i in range(10)]
                writer.writerow(header)

            row = [participant_id, trial, gender, group, age, current_time, self.trial_types]
            row.extend(self.reaction_times)
            row.extend(self.correctness)
            writer.writerow(row)

    def run_test(self, participant_id, trial, group, gender, age, current_time, practice=False):
        running = True
        trial_count = 0
        total_trials = 5 if practice else 20

        while running and trial_count < total_trials:
            self.show_continue_message()
            self.screen.fill(WHITE)

            target_color_name = random.choice(self.color_names)
            target_ink_color = self.colors[target_color_name]
            compatible = random.choices([True, False], weights=[0.2, 0.8])[0]

            if not compatible:
                possible_ink_colors = [color for name, color in self.colors.items() if name != target_color_name]
                target_ink_color = random.choice(possible_ink_colors)

            self.trial_types.append("True" if compatible else "False")
            target_ink_color_name = [name for name, color in self.colors.items() if color == target_ink_color][0]
            self.draw_color_word(target_color_name, target_ink_color)
            buttons = self.draw_color_buttons(target_ink_color_name)
            pygame.display.flip()

            start_time = time.time()
            clicked = False

            while not clicked:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        clicked = True
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        for button_rect, color_name in buttons:
                            if button_rect.collidepoint(pos):
                                reaction_time = time.time() - start_time
                                self.reaction_times.append(reaction_time)

                                if color_name == target_ink_color_name:
                                    self.correctness.append("Correct")
                                else:
                                    self.correctness.append("Incorrect")
                                clicked = True
                                break

            trial_count += 1
            pygame.time.delay(500)
            self.show_continue_message()

        if not practice:
            self.save_reaction_times(participant_id, trial, group, gender, age, current_time)

    def show_continue_message(self):
        """Displays a black circle with instructions for the user to click to continue."""
        self.screen.fill(WHITE)
        circle_position = (self.screen_width // 2, 250)
        circle_radius = 100
        pygame.draw.circle(self.screen, BLACK, circle_position, circle_radius)

        message = "Press the black circle to start new trial"
        text_surface = self.font.render(message, True, BLACK)
        text_rect = text_surface.get_rect(center=(self.screen_width // 2, circle_position[1] + 150))
        self.screen.blit(text_surface, text_rect)

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    distance = ((pos[0] - circle_position[0]) ** 2 + (pos[1] - circle_position[1]) ** 2) ** 0.5
                    if distance <= circle_radius:
                        waiting = False

if __name__ == "__main__":
    test = StroopTest()
    practice = True
    gender = "M"
    age = 29
    group = "exercise"
    current_time = datetime.now().strftime("%H:%M:%S")
    participant_id = 7
    trial = 1

    if not test.check_if_exists(participant_id, trial):
        test.run_test(participant_id, trial, group, gender, age, current_time, practice)
