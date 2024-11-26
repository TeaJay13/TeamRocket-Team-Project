import sqlite3

# Initialize the database
def initialize_db():
    conn = sqlite3.connect('game_scores.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scoreboard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            score INTEGER NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Save the score and username to the database
def save_score(username, score):
    conn = sqlite3.connect('game_scores.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO scoreboard (username, score) VALUES (?, ?)", (username, score))
    conn.commit()
    conn.close()
    print(f"Saved: {username} - {score}")

# Retrieve the top 10 scores and return them as a list
def display_high_scores():
    conn = sqlite3.connect('game_scores.db')
    cursor = conn.cursor()
    cursor.execute("SELECT username, score, timestamp FROM scoreboard ORDER BY score DESC LIMIT 10")
    scores = cursor.fetchall()
    conn.close()

    # If no scores exist, return an empty list
    if not scores:
        return []

    return scores
