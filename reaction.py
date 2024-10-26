import pygame
import random
import time
import sys
import csv
from datetime import datetime

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


class ReactionTimeTest():
    def __init__(self):
        pygame.init()
        self.font = pygame.font.Font(None, 90)
        self.small_font = pygame.font.Font(None, 40)
        self.screen_width = 1500
        self.screen_height = 800
        # Set window
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Reaction Time Test")

    def check_if_exists(self, id, trial):
        """Check if the given id and trial already exists in the CSV file."""
        try:
            with open("reaction_times.csv", "r") as f:
                reader = csv.reader(f)
                header = next(reader)  # Read the header

                # Iterate over each row in the CSV
                for row in reader:
                    if row[0] == str(id) and int(row[1]) == trial:
                        print(f"ID {id} and Trial {trial} already exist.")  # Print statement
                        return True  # Found matching ID and trial
        except FileNotFoundError:
             return False  
        return False  # ID and trial do not exist
    
    def draw_text(self,text, font, color, x, y):
        """Render text on screen"""
        screen_text = font.render(text, True, color)
        text_rect = screen_text.get_rect(center=(x, y))
        self.screen.blit(screen_text, text_rect)
    

    def save_reaction_times(self, reaction_times, id, trial, gender, age, current_time):
        """Save reaction times to a CSV file, appending new data"""

        with open("reaction_times.csv", "a", newline='') as f:
            writer = csv.writer(f)
            # If the file is empty, write the header
            if f.tell() == 0:  
                tries = [i for i in range(1,20)]
                writer.writerow(["id", "trial", "gender", "age", "time", tries]) 

            
            reaction_times = reaction_times + [None] * (20 - len(reaction_times))  # Fill the rest with None
            writer.writerow([id, trial, gender, age, current_time, reaction_times])

    def reaction_time_test(self, id, trial, gender, age, current_time, practice=False):
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
            self.screen.fill(WHITE)
            self.draw_text("Press space to start", self.font, BLACK, self.screen_width /2, self.screen_height /2)
            #self.draw_text("Reopen the game to reset", self.small_font, BLACK, 150, 300)
            pygame.display.flip()

            # Wait for user input
            while not waiting_for_go and not waiting_for_reaction and running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE and not waiting_for_go and not waiting_for_reaction:
                            # Display "Wait..." in black
                            self.screen.fill(WHITE)
                            circle_center = (self.screen_width/2, self.screen_height/2)  # Center of the circle
                            circle_radius = 200  # Radius of the circle
                            pygame.draw.circle(self.screen, RED, circle_center, circle_radius)  # Draw the circle
                            self.draw_text("Wait...", self.font, WHITE, self.screen_width /2, self.screen_height /2)
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
                                self.screen.fill(WHITE)
                                self.draw_text("Too Soon!", self.font, RED, self.screen_width /2, self.screen_height /2)
                                pygame.display.flip()
                                pygame.time.delay(1000)

                                # Return to "Wait..." screen
                                self.screen.fill(WHITE)
                                pygame.draw.circle(self.screen, RED, circle_center, circle_radius)  # Draw the circle
                                self.draw_text("Wait...", self.font, WHITE, self.screen_width /2, self.screen_height /2)
                                pygame.display.flip()
                                pygame.time.delay(2000)  # Display "Wait..." again for 2 seconds
                                break

                # If the random delay has passed, show "GO!"
                if time.time() >= go_time:
                    self.screen.fill(WHITE)
                    circle_center = (self.screen_width/2, self.screen_height/2)  # Center of the circle
                    circle_radius = 200  # Radius of the circle
                    pygame.draw.circle(self.screen, GREEN, circle_center, circle_radius)  # Draw the circle
                    self.draw_text("GO!", self.font, RED,self.screen_width /2, self.screen_height /2)
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
                            self.screen.fill(WHITE)
                            #self.draw_text(f"Reaction: {reaction_time:.3f} s", self.small_font, RED, self.screen_width /2, self.screen_height /2)
                            self.draw_text(f"Trial: {trial_count}", self.small_font, BLACK, self.screen_width /2, self.screen_height /2 )
                            self.draw_text("Wait for next trial", self.small_font, BLACK, self.screen_width /2, self.screen_height /2 + 50)
                            pygame.display.flip()
                            pygame.time.delay(2000)  # Display the result for 3 seconds
                            waiting_for_reaction = False  # Reset the test

            pygame.display.update()
        print(reaction_times)
        if not practice:
            self.save_reaction_times(reaction_times, id, trial, gender, age, current_time)

        # Print collected data when the test is closed
        pygame.quit()
        print("Test finished.")

        
        

if __name__ == "__main__":
    test = ReactionTimeTest()
    practice = True
    gender = "M" 
    age = 29
    current_time = datetime.now().strftime("%H:%M:%S")
    id = 3
    trial = 1

    if test.check_if_exists(id,trial) == False:
        test.reaction_time_test(id, trial, gender, age, current_time, practice)
    

