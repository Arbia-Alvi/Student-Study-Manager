
## 1. Project Overview

**Student Study Manager** is a web-based application developed to help students organize their academic work, manage study subjects, track tasks, and monitor their study progress in one place.

Students often have multiple assignments, deadlines, and study activities to manage. This application provides a simple and user-friendly interface where students can create tasks, set priorities, manage due dates, and track completed and pending work.

The application is developed using Python and Flask for the backend, SQLite for database storage, and HTML, CSS, Bootstrap, and Jinja2 templates for the user interface.

## 2. Project Objectives

The main objectives of this project are:

- To help students organize their daily study activities.
- To provide a convenient way to manage subjects and academic tasks.
- To help students track assignment deadlines.
- To identify overdue, upcoming, and due-today tasks.
- To monitor completed and pending work.
- To display study progress through a dashboard.
- To keep each user's study information separate from other users.
- To provide a simple and accessible web-based study management system.

## 3. Key Features

### 3.1 User Authentication
- User registration and login.
- Logout functionality.
- Password management.
- Access to personal study information through an authenticated account.

### 3.2 Subject Management
- View and manage study subjects.
- Add subjects to organize academic work.
- Edit subject details.
- Delete subjects.
- Provide default programming subjects to newly registered users.

### 3.3 Task Management
- Create new study tasks.
- Edit task details.
- Delete tasks.
- Mark tasks as completed.
- Track pending and completed tasks.
- Assign a priority level to each task.
- Set due dates for study activities.

### 3.4 Task Search and Filtering
- Search tasks by title or description.
- Filter tasks by priority: Low, Medium, and High.
- Filter tasks by status: Pending and Completed.
- Sort tasks by newest first, due date, or priority.
- Clear search and filter selections.

### 3.5 Dashboard and Study Progress
The dashboard provides an overview of study activities, including:

- Total Subjects
- Total Tasks
- Completed Tasks
- Pending Tasks
- Overdue Tasks
- Tasks Due Today
- Upcoming Tasks
- Study Progress percentage

These statistics help users understand their current workload and monitor their progress.

### 3.6 Profile Management
- View personal profile information.
- Edit profile details.
- Change account password.

### 3.7 Data Import and Export
The application includes JSON import/export functionality to support transferring study information. It also includes API-related functionality for working with application data.

## 4. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Flask | Web application framework |
| SQLite | Database management |
| HTML5 | Web page structure |
| CSS3 | Styling and layout |
| Bootstrap | Responsive interface and UI components |
| Jinja2 | Dynamic HTML templates |
| Flask-Login | User authentication and session management |
| SQLAlchemy | Database models and queries |
| JSON | Data import and export |

## 5. Application Structure

The project is organized into separate files and folders to make the code easier to manage.

- `app.py` — Main application entry point.
- `models/` — Database models for users, subjects, and tasks.
- `routes/` — Application routes for authentication, dashboard, subjects, and tasks.
- `templates/` — HTML templates for the user interface.
- `instance/` — Local application database and related instance files.
- `venv/` — Python virtual environment used for project dependencies.
- `requirements.txt` — Project dependency list, if included.

## 6. How to Install and Run

### Prerequisites
- Python installed on the computer.
- A code editor such as Visual Studio Code.
- A web browser.

### Installation Steps

1. Open the project folder in Visual Studio Code.
2. Open the terminal in the project directory.
3. Create a virtual environment if one does not already exist:

   `python -m venv venv`

4. Activate the virtual environment on Windows:

   `venv\Scripts\activate`

5. Install the required packages, if `requirements.txt` exists:

   `pip install -r requirements.txt`

6. Run the application:

   `python app.py`

7. Open the following address in your web browser:

   `http://127.0.0.1:8000`

8. Register an account or log in to start managing study subjects and tasks.

## 7. Database

The application uses SQLite to store user accounts, subjects, and study tasks. Database models organize the information and support operations such as creating, viewing, updating, and deleting records.

User-specific filtering is used in relevant subject and task routes to help prevent one user from accessing another user's records through those routes.

## 8. Security Considerations

- Authentication is required for protected application pages.
- Subject and task queries use ownership checks in relevant routes.
- Password changes and account management should be performed through the application's authenticated interface.
- Database backups should be maintained before making major database changes.

## 9. Benefits of the Project

- Helps students manage academic responsibilities.
- Makes task deadlines easier to track.
- Improves organization and time management.
- Provides a quick overview of study progress.
- Keeps subjects and tasks organized in a single application.
- Demonstrates practical use of Python, Flask, database operations, and web development.

## 10. Future Improvements

Possible future enhancements include:

- Email or browser reminders for upcoming deadlines.
- Calendar-based task visualization.
- More detailed progress reports.
- Additional dashboard charts.
- Improved mobile interface.
- More flexible subject categories.
- Automated database backup and recovery options.

## 11. Conclusion

Student Study Manager is designed to make academic task management easier and more organized. By combining subject management, task tracking, deadlines, priorities, search and filtering, and progress statistics, the application provides students with a convenient way to manage their study activities.

The project also demonstrates the practical application of Python, Flask, SQLite, and modern web technologies in developing a database-driven web application.