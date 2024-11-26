import time
import pygame

# Initialize scoring variables
start_time = None
current_time = 0
total_score = 0
POINTS_PER_INTERVAL = 10
INTERVAL_DURATION = 10  # Award points every 10 seconds

# Start the timer (call this at the beginning of the game)
def start_timer():
    global start_time, current_time, total_score
    start_time = time.time()
    current_time = 0
    total_score = 0
    print("Timer started.")

# Update the timer and calculate score (call this in the game loop)
def update_timer():
    global current_time, total_score
    elapsed_time = int(time.time() - start_time)
    current_time = elapsed_time

    # Award points every INTERVAL_DURATION seconds
    total_score = (elapsed_time // INTERVAL_DURATION) * POINTS_PER_INTERVAL

# Display the timer and score on the screen
def display_timer_and_score(screen, font):
    # Timer in the format mm:ss
    minutes = current_time // 60
    seconds = current_time % 60
    timer_text = f"Time: {minutes:02}:{seconds:02}"
    score_text = f"Score: {total_score}"

    # Render timer and score
    timer_surface = font.render(timer_text, True, (255, 255, 255))
    score_surface = font.render(score_text, True, (255, 255, 255))

    # Display in the top-left corner
    screen.blit(timer_surface, (10, 10))
    screen.blit(score_surface, (10, 40))

# Finalize the score when the player dies
def get_final_score():
    print(f"Final Score: {total_score}")
    return total_score
