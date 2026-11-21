# 🎓 Campus Opportunity Verification Portal

A lightweight, beginner-friendly web application designed for college campuses to help students discover genuine hackathons, technical workshops, and coding competitions while protecting them from unverified links and misleading social media forwards.

---

## 📌 1. Problem Statement

College students frequently encounter hackathon and workshop announcements across informal channels like WhatsApp groups, Telegram channels, and Instagram stories. Many of these links:
* Require unexpected registration fees.
* Lead to phishing or credential-harvesting forms.
* Lack verified faculty or institutional backing.

**The Solution:** The **Campus Opportunity Verification Portal** provides a centralized, human-verified repository. Every submitted opportunity includes its origin source and an explicit verification status:
* 🟢 **Verified**: Confirmed through official college notices, verified faculty circulars, or recognized clubs.
* 🟡 **Needs Review**: Submitted by a student or organizer, awaiting administrator review.
* ⚪ **Unverified**: Sourced from unverified external forwards; students are warned before proceeding.

---

## 🚀 2. Key Features

1. **Student Catalog & Event Cards**:
   * Displays all upcoming opportunities with organizer names, dates, sources, and verification badges.
2. **Instant Keyword Search**:
   * Search through event titles, organizers, sources, and descriptions in real time.
3. **Status Filters**:
   * One-click filters to display *All Events*, *Verified Only*, *Needs Review*, or *Unverified*.
4. **Dedicated Event Details Page (`/event/<id>`)**:
   * Deep dive into an event's full description, verification breakdown, and student safety checklist.
5. **Opportunity Submission Form (`/add`)**:
   * Students or organizers can submit events. All submissions default to **Needs Review** for student safety.
6. **Administrator Dashboard (`/admin`)**:
   * College coordinators can review submissions and update verification statuses with a single click.

---

## 🛠️ 3. Technologies Used

* **Language**: Python 3
* **Web Framework**: [Flask](https://flask.palletsprojects.com/) (Lightweight WSGI web application framework)
* **Database**: SQLite3 (Serverless, zero-configuration database built directly into Python)
* **Frontend**: HTML5, Vanilla CSS3, and Jinja2 Template Engine

---

## 📂 4. Project Directory Structure

```text
campus_portal/
│
├── app.py                  # Main Flask application: URL routes and business logic
├── database.py             # SQLite helper functions: table initialization, CRUD operations
├── events.db               # SQLite database file storing persistent records
├── requirements.txt        # Python dependency manifest (Flask)
├── run.bat                 # One-click Windows starter script
├── README.md               # Complete project documentation & viva guide
│
├── templates/              # HTML frontend templates (Jinja2)
│   ├── base.html           # Master layout with navbar, alerts, and footer
│   ├── index.html          # Public catalog with search bar and filter badges
│   ├── event_detail.html   # Detailed event view with verification breakdown
│   ├── add_event.html      # Opportunity submission form
│   └── admin.html          # Administrator verification control panel
│
└── static/
    └── style.css           # Clean, responsive CSS styling and status badge colors
```

---

## 💻 5. How to Run on Your Computer

### Prerequisites
* Windows 10/11 with Python installed.

### Step 1: Open Terminal
Open PowerShell or Command Prompt and navigate to the project directory:
```powershell
Set-Location "c:\Users\Vaishalee S\Desktop\python\campus_portal"
```

### Step 2: Run the Application
You can run it in either of two easy ways:

* **Method A (Command)**:
  ```powershell
  .\.venv\Scripts\python.exe app.py
  ```
* **Method B (1-Click)**:
  Simply double-click the **`run.bat`** file in your project folder!

The app will start and automatically open your default browser to:
**`http://127.0.0.1:5000`**

---

## 🗄️ 6. Database Schema

The database uses a single table named `events`:

| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | `PRIMARY KEY AUTOINCREMENT` | Unique identifier for each event |
| `name` | `TEXT` | `NOT NULL` | Name of the hackathon or workshop |
| `organizer` | `TEXT` | `NOT NULL` | Organizing club, department, or company |
| `event_date` | `TEXT` | `NOT NULL` | Date of the opportunity |
| `registration_link` | `TEXT` | `NOT NULL` | External registration URL |
| `source` | `TEXT` | `NOT NULL` | Reported source (e.g., Notice Board, WhatsApp) |
| `status` | `TEXT` | `CHECK(status IN ('Verified', 'Unverified', 'Needs review'))` | Verification state |
| `description` | `TEXT` | `DEFAULT 'No additional description provided.'` | Full event overview |
| `created_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | Submission timestamp |

---

## 🎓 7. Top 10 Viva & Evaluation Questions (With Answers)

### Q1: Why did you choose Flask over Django?
> **Answer**: Flask is a lightweight micro-framework. It allows us to build simple, modular web applications without the heavy boilerplate or strict configurations of Django. For a beginner project focused on core Python, routing, and SQLite, Flask is more transparent and easier to understand.

### Q2: What is SQLite, and why is it suitable for this project?
> **Answer**: SQLite is a self-contained, serverless, zero-configuration database engine. The entire database is stored in a single file on disk (`events.db`). Python includes the `sqlite3` module by default, eliminating the need to set up external database servers like MySQL or PostgreSQL during development.

### Q3: What is the purpose of `conn.row_factory = sqlite3.Row`?
> **Answer**: By default, SQLite returns rows as tuples (e.g. `row[0]`, `row[1]`), which can cause errors if columns change. `sqlite3.Row` allows dictionary-like column access by name (e.g. `row['name']`), making the code readable and maintainable.

### Q4: How does parameterization (`?`) in SQL queries prevent SQL Injection?
> **Answer**: Instead of concatenating user input directly into SQL strings (which allows attackers to inject malicious SQL commands), we pass inputs as parameters with `?` placeholders (e.g. `WHERE id = ?`). SQLite treats the input strictly as literal values, completely neutralizing SQL injection attacks.

### Q5: What is Jinja2 Template Inheritance?
> **Answer**: Jinja2 lets child templates (like `index.html` and `admin.html`) extend a parent template (`base.html`). The parent template contains common elements like the navigation bar and stylesheet links, while child templates only define page-specific content blocks (`{% block content %}`). This follows the DRY (Don't Repeat Yourself) principle.

### Q6: What is the difference between HTTP `GET` and `POST` in this application?
> **Answer**:
> * `GET` is used to retrieve data without modifying server state (e.g., viewing `/` or searching `/?q=AI`).
> * `POST` is used to send sensitive data to the server that modifies the database (e.g., submitting `/add` or updating a status at `/admin/update/<id>`).

### Q7: Why do newly submitted opportunities default to "Needs review"?
> **Answer**: This is a core student safety design decision. If users could submit links that were automatically marked as "Verified", malicious actors could spread phishing links. Defaulting to "Needs review" ensures that every link undergoes administrative verification before gaining a trusted status.

### Q8: What does Flask's `flash()` function do?
> **Answer**: `flash()` allows Flask to pass temporary feedback messages (such as *"Opportunity submitted!"* or *"Status updated!"*) from one route to the next page render, where Jinja displays them inside alert banners.

### Q9: How does the search feature work behind the scenes?
> **Answer**: The user submits a query `q`. The backend runs a parameterized SQL query with the `LIKE` operator (`%query%`) matching against the `name`, `organizer`, `source`, and `description` columns, returning any records that contain the keyword.

### Q10: How can this project be scaled or improved in the future?
> **Answer**:
> 1. Adding administrator authentication with password hashing (`Werkzeug.security`).
> 2. Email or SMS alerts when a new opportunity from a student's preferred club is verified.
> 3. Allowing students to bookmark or upvote opportunities.
