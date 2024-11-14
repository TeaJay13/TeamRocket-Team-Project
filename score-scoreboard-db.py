import sqlite3
import time

# Initialize score variables
enemy_score = 0
time_score = 0
start_time = time.time()  # Track when the game started

# Constants for time-based scoring
POINTS_PER_INTERVAL = 10
INTERVAL_DURATION = 30  # Every 30 seconds

# Connect to SQLite and set up the scores table
def initialize_db():
    conn = sqlite3.connect('game_scores.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scoreboard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            enemy_score INTEGER,
            time_score INTEGER,
            total_score INTEGER,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Function to increment enemy score
def add_enemy_score(points=1):
    global enemy_score
    enemy_score += points
    print(f"Enemy score: {enemy_score}")

    # TODO: Connect with game logic to add points when an enemy is killed
    # Example:
    # Call `add_enemy_score()` in your game whenever an enemy is defeated
    # score_system.add_enemy_score(points)

# Function to update time score based on elapsed time
def update_time_score():
    global time_score
    current_time = time.time()
    elapsed_time = int(current_time - start_time)

    # Award points every 30 seconds
    intervals = elapsed_time // INTERVAL_DURATION
    time_score = intervals * POINTS_PER_INTERVAL
    print(f"Time score: {time_score}")

    # TODO: Call this function regularly in the main game loop to keep the time score updated
    # Example:
    # In your main game loop, call `update_time_score()` to accumulate survival points

# Function to calculate and save total score to the database
def save_score():
    total_score = enemy_score + time_score
    conn = sqlite3.connect('game_scores.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO scoreboard (enemy_score, time_score, total_score) VALUES (?, ?, ?)",
                   (enemy_score, time_score, total_score))
    conn.commit()
    conn.close()
    print(f"Score saved: Enemy - {enemy_score}, Time - {time_score}, Total - {total_score}")

    # TODO: Trigger `save_score()` when the game ends, before returning to the main menu or end screen
    # Example:
    # If using an end screen module, call `score_system.save_score()` in that module

# Function to reset scores (for a new game)
def reset_scores():
    global enemy_score, time_score, start_time
    enemy_score = 0
    time_score = 0
    start_time = time.time()  # Reset start time
    print("Scores reset.")

    # TODO: Call `reset_scores()` at the start of a new game to reset all scores
    # Example:
    # In your start menu or game start logic, call `score_system.reset_scores()` to reset scores

# Function to load and display the scoreboard
def display_scoreboard():
    conn = sqlite3.connect('game_scores.db')
    cursor = conn.cursor()
    cursor.execute("SELECT enemy_score, time_score, total_score, timestamp FROM scoreboard ORDER BY total_score DESC LIMIT 10")
    scores = cursor.fetchall()
    conn.close()

    # Print the scores (You can replace this with rendering in Pygame if needed)
    print("Top Scores:")
    for idx, (enemy, time, total, timestamp) in enumerate(scores, start=1):
        print(f"{idx}. Enemy Score: {enemy}, Time Score: {time}, Total: {total}, Date: {timestamp}")

    # TODO: Integrate `display_scoreboard()` with Pygame or end screen for an in-game display
    # Example:
    # In the end screen, call `score_system.display_scoreboard()` to show top scores on screen

# Initialize the database on import
initialize_db()
