"""
database.py
-----------
Handles all interactions with our SQLite database (events.db).

This file is responsible for:
1. Connecting to the SQLite database.
2. Creating and upgrading the 'events' table.
3. Providing helper functions to add, retrieve, search, and update events.
"""

import os
import sqlite3

# Define the path to our SQLite database file inside the campus_portal folder
DB_PATH = os.path.join(os.path.dirname(__file__), "events.db")


def get_db_connection():
    """
    Creates and returns a connection to the SQLite database.
    Using sqlite3.Row allows accessing column values by name (event['name']).
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    Initializes the database table, adds new columns if needed,
    and inserts sample events if the table is newly created.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create the events table if it does not exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            organizer TEXT NOT NULL,
            event_date TEXT NOT NULL,
            registration_link TEXT NOT NULL,
            source TEXT NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('Verified', 'Unverified', 'Needs review')),
            description TEXT DEFAULT 'No additional description provided.',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Check if 'description' column exists in case the table was created earlier
    cursor.execute("PRAGMA table_info(events)")
    columns = [col["name"] for col in cursor.fetchall()]
    if "description" not in columns:
        cursor.execute("ALTER TABLE events ADD COLUMN description TEXT DEFAULT 'No additional description provided.'")
        conn.commit()

    # Check if there are already events
    cursor.execute("SELECT COUNT(*) AS count FROM events")
    count = cursor.fetchone()["count"]

    if count == 0:
        sample_events = [
            (
                "National AI Hackathon 2026",
                "Computer Science Department",
                "2026-12-10",
                "https://example.com/ai-hackathon",
                "Official College Circular & Notice Board",
                "Verified",
                "A 24-hour national hackathon focused on Artificial Intelligence and Machine Learning solutions for campus sustainability. Open to all engineering students with prizes worth Rs. 50,000."
            ),
            (
                "Intro to Web Development Workshop",
                "Coding Club",
                "2026-12-15",
                "https://example.com/web-workshop",
                "College Discord Server",
                "Needs review",
                "A hands-on weekend workshop covering HTML, CSS, JavaScript, and beginner Python web development with Flask. Certificate provided to attendees upon completion."
            ),
            (
                "Free Laptop Crypto Challenge",
                "Unknown Promoter",
                "2026-12-20",
                "https://example.com/suspicious-link",
                "Random WhatsApp Group Forward",
                "Unverified",
                "Claims to give away free laptops and crypto tokens for sharing a Telegram invite link. Caution: unverified source with suspicious prerequisites."
            )
        ]

        cursor.executemany("""
            INSERT INTO events (name, organizer, event_date, registration_link, source, status, description)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, sample_events)

        conn.commit()
        print("Database initialized with sample events.")
    else:
        conn.commit()

    conn.close()


def get_all_events(status_filter=None, search_query=None):
    """
    Fetches events with optional keyword search and status filter.
    Search looks across name, organizer, source, and description.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    conditions = []
    params = []

    # Filter by verification status if selected
    if status_filter and status_filter in ["Verified", "Unverified", "Needs review"]:
        conditions.append("status = ?")
        params.append(status_filter)

    # Search query across multiple fields
    if search_query:
        query_pattern = f"%{search_query.strip()}%"
        conditions.append("(name LIKE ? OR organizer LIKE ? OR source LIKE ? OR description LIKE ?)")
        params.extend([query_pattern, query_pattern, query_pattern, query_pattern])

    sql = "SELECT * FROM events"
    if conditions:
        sql += " WHERE " + " AND ".join(conditions)
    sql += " ORDER BY event_date ASC"

    cursor.execute(sql, params)
    events = cursor.fetchall()
    conn.close()
    return events


def get_event_by_id(event_id):
    """Fetches a single event by its unique ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events WHERE id = ?", (event_id,))
    event = cursor.fetchone()
    conn.close()
    return event


def add_event(name, organizer, event_date, registration_link, source, status="Needs review", description=""):
    """Inserts a newly submitted event into the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    if not description:
        description = "No additional description provided."

    cursor.execute("""
        INSERT INTO events (name, organizer, event_date, registration_link, source, status, description)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, organizer, event_date, registration_link, source, status, description))
    conn.commit()
    conn.close()


def update_event_status(event_id, new_status):
    """Updates the verification status of an existing event."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE events
        SET status = ?
        WHERE id = ?
    """, (new_status, event_id))
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
