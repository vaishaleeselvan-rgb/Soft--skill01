"""
app.py
------
The main Flask web application for the Campus Opportunity Verification Portal.

Features:
1. '/' (Home): Browse hackathons & workshops with keyword search and status filters.
2. '/event/<id>' (Event Details): Full page with description, verification checklist, & registration link.
3. '/add' (Submit Opportunity): Form to submit events with title, organizer, date, link, source, & description.
4. '/admin' (Admin Dashboard): Manage events and update verification statuses.
5. '/admin/update/<id>' (Update Status): Process status updates.
"""

import os
import threading
import webbrowser
from flask import Flask, render_template, request, redirect, url_for, flash
import database

# Initialize the Flask application
app = Flask(__name__)

# Secret key required for session security and flash notifications
app.secret_key = "campus-opportunity-verification-secret"

# Make sure database and tables exist when starting the app
database.init_db()


@app.route("/")
def index():
    """
    Home page for students.
    Supports filtering by status (?status=Verified) and keyword search (?q=AI).
    """
    selected_status = request.args.get("status", "All")
    search_query = request.args.get("q", "").strip()

    status_filter = selected_status if selected_status in ["Verified", "Unverified", "Needs review"] else None
    events = database.get_all_events(status_filter=status_filter, search_query=search_query)

    return render_template(
        "index.html",
        events=events,
        current_filter=selected_status,
        search_query=search_query
    )


@app.route("/event/<int:event_id>")
def event_detail(event_id):
    """
    Detailed event view page.
    Displays full description, organizer details, source verification notes,
    student safety tips, and the link to register.
    """
    event = database.get_event_by_id(event_id)
    if not event:
        flash("Event not found.", "error")
        return redirect(url_for("index"))

    return render_template("event_detail.html", event=event)


@app.route("/add", methods=["GET", "POST"])
def add():
    """
    Page to submit a new event.
    - GET: displays submission form.
    - POST: validates inputs and saves to database with default 'Needs review' status.
    """
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        organizer = request.form.get("organizer", "").strip()
        event_date = request.form.get("event_date", "").strip()
        registration_link = request.form.get("registration_link", "").strip()
        source = request.form.get("source", "").strip()
        description = request.form.get("description", "").strip()

        # Simple validation
        if not name or not organizer or not event_date or not registration_link or not source:
            flash("Please fill in all required fields (Name, Organizer, Date, Link, and Source).", "error")
            return render_template("add_event.html")

        # Automatically add https:// if the user typed example.com or www.example.com
        if not (registration_link.startswith("http://") or registration_link.startswith("https://")):
            registration_link = "https://" + registration_link

        # Newly submitted events default to 'Needs review' for student safety
        database.add_event(
            name=name,
            organizer=organizer,
            event_date=event_date,
            registration_link=registration_link,
            source=source,
            status="Needs review",
            description=description
        )

        flash("Opportunity submitted! It is currently marked as 'Needs review' pending admin verification.", "success")
        return redirect(url_for("index"))

    return render_template("add_event.html")


@app.route("/admin")
def admin():
    """
    Admin dashboard page.
    Displays all events in an administrative table.
    """
    events = database.get_all_events()
    return render_template("admin.html", events=events)


@app.route("/admin/update/<int:event_id>", methods=["POST"])
def update_status(event_id):
    """
    Processes the status update form submitted by an administrator.
    """
    new_status = request.form.get("status")

    if new_status in ["Verified", "Unverified", "Needs review"]:
        database.update_event_status(event_id, new_status)
        flash(f"Status for event #{event_id} was successfully updated to '{new_status}'.", "success")
    else:
        flash("Invalid status choice.", "error")

    return redirect(url_for("admin"))


if __name__ == "__main__":
    # Open browser automatically once the server is ready
    if not app.debug or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        print("\nOpening http://127.0.0.1:5000 in your web browser...")
        threading.Timer(1.2, lambda: webbrowser.open("http://127.0.0.1:5000")).start()

    print("Starting Campus Opportunity Verification Portal on http://127.0.0.1:5000 ...")
    app.run(debug=True, port=5000)
