# YuLearn – Study Tracker
#### Video Demo:  https://youtu.be/MDfrDW2obuA
#### Description:

YuLearn is a web application built using Python, Flask, Javascript, HTML, CSS and Bootstrap. It functions as a study organizer that allows users to create routines, track study time, take notes, and monitor their progress visually and interactively. The app is ideal for students who want to improve their productivity and maintain a consistent study routine.

### Key Features

- User Registration and Login: Anyone can create an account to start tracking their study activities.

- Study Planner: Users can create study routines and add multiple subjects to each routine.

- Study Timer: While studying, users can start a timer to track their study time, add notes related to the session, and pause or reset the timer.

- Notes: All notes taken during study sessions are saved and can be accessed on a dedicated notes page.

- Progress Tracking: The app generates visual summaries, showing total study hours, top 5 studied subjects, and total time spent per routine.

- Study History: Every study session is logged with time spent, notes, and the associated subject.

#### HTML File Structure

1. home.html
The home page includes a welcome message, a motivational text, and a button that directs users to the planner. An illustrative image is also displayed.

2. planner.html
Displays all the routines created by the user in responsive cards. Each card shows the routine title, associated subjects, and buttons to edit, delete, or start the routine. Includes an expandable form for adding new routines and subjects.

3. plan.html
Shows the details of a specific routine, including all associated subjects and estimated study time. Users can navigate through subjects and start study sessions.

4. edit.html
Allows editing the routine title, updating descriptions for existing subjects, and adding new subjects to the routine.

5. study.html
The study session page with an upward-counting timer. Includes buttons to start, pause, and reset the timer. Users can also add optional notes for the session. The recorded time and notes are saved in the StudyLog table.

6. progress.html
Displays graphs and key statistics about user progress: total study time, top 5 subjects studied, and total time per routine. The top three subjects are highlighted in gold, silver, and bronze for clarity.

7. notes.html
Shows all notes saved by the user, including those created during study sessions and general notes. Each note is displayed in a responsive card with the title, content, date, and study time (if applicable).

8. apology.html
Used to display error messages or feedback. Shows a status code and a formatted message to the user.

9. helpers.py

Contains utility functions:

login_required(f): A decorator that protects routes and requires the user to be logged in. If the user is not logged in, they are redirected to the login page.

apology(message, code=400): Renders a custom error message using apology.html, escaping special characters to avoid rendering issues.

10. app.py

##### The main application file. Includes:

Flask and SQLAlchemy configuration.

Data models: User, Routine, Subject, RoutineSubject, StudyLog, and Note.

#### Main routes:

- / → home

- /login, /logout, /register → authentication

- /planner → view and create routines

- /plan and /plan/<int:routine_id>/edit → view and edit routines

- /plan/<int:routine_id>/delete → delete a routine

- /study/<int:routine_id> → upward-counting study timer with optional notes

- /progress → user progress page

- /notes → view saved notes

The app.py also includes helper functions to prevent caching in the browser and manage user sessions.

##### Database

- User: Stores user account information.

- Routine: Stores study routines associated with each user.

- Subject: Stores subjects added to routines.

- RoutineSubject: Many-to-many relationship linking routines and subjects.

- StudyLog: Records each study session, including time spent and optional notes.

- Note: Stores general notes or notes created during study sessions.

##### Technology Stack

- Python

- Flask

- SQLAlchemy

- SQLite

- JavaScript

- HTML5

- CSS3

- Bootstrap

##### Installation
    For installation you must install Git, and run with it, even in Windows.

1. Clone the repository:
    
    ```
    git clone https://github.com/yurirampazo/CS50-Final-Project.git
    ``` 

2. Create and activate a virtual environment:

    ```
    python -m venv venv
    source venv/bin/activate
    ```

3. Install dependencies:
    ```
    pip install -r requirements.txt
    ```

4. Run the application:
    ```
    flask run
    ```


5. Access it in your browser: http://127.0.0.1:5000/

Usage

1. Register a new account or log in.

2. Create routines in the planner and add subjects with optional descriptions.

3. Click Start to begin a study session.

4. Add notes during the session if desired.

5. Pause or reset the timer as needed.

6. Track your progress on the Progress page and view all notes on the Notes page.

YuLearn combines organization, time tracking, and note-taking to provide users with a clear overview of their learning progress. It encourages consistent study habits and helps students visualize and improve their productivity. Hope you enjoy it!
