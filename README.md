# Task-management-web-app
A web-based task management application with user authentication, task assignment, status tracking, and full CRUD operations – built with Streamlit and SQLite.

# Streamlit Task Management System

## Overview
This is a full-featured task management web application built with **Streamlit** (frontend) and **SQLite** (backend). It allows users to create accounts, assign tasks to team members, track task status, and modify or delete tasks as needed.

## Features

### User Authentication
- **Login** – Existing users can sign in with their User ID and password
- **Sign Up** – New users can create an account with User ID, password, and email
- Duplicate User ID/email prevention with database integrity checks

### Task Management
| Feature | Description |
|---------|-------------|
| **Define Task** | Create a new task with name, description, priority (1-5), and assign to any registered user |
| **View Tasks** | See all tasks assigned to YOU with current status (waiting/done) |
| **Check Tasks** | View all tasks YOU created for others (to monitor progress) |
| **Change Task** | Modify or delete tasks you created (only if status is still 'new') |
| **Update Status** | Mark assigned tasks as "waiting" or "done" (strikethrough for completed tasks) |

### Task States
Tasks flow through these statuses:
- **new** – Just created, not yet assigned/started (can be edited/deleted)
- **waiting** – Assigned and pending completion
- **done** – Completed (task displays with strikethrough formatting)

### Database Schema

#### User Table
| Column | Type | Description |
|--------|------|-------------|
| user_id | TEXT (PRIMARY KEY) | Unique login identifier |
| user_pass | TEXT | User password |
| email | TEXT (UNIQUE) | User's email address |

#### Task Table
| Column | Type | Description |
|--------|------|-------------|
| task_id | TEXT (PRIMARY KEY) | Auto-incremented task ID |
| task_name | TEXT | Task title |
| description | TEXT | Detailed task description |
| priority | TEXT | Priority level (1-5, 1=highest) |
| assigned_user | TEXT (FOREIGN KEY) | User responsible for the task |
| creator | TEXT (FOREIGN KEY) | User who created the task |
| status | TEXT | 'new', 'waiting', or 'done' |

## Installation

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/task-management-system.git
cd task-management-system
```

2. Install requirements:
pip install streamlit

3. Create the database:
Ensure new_db.db exists at D:/python projects/new_db.db Or modify the database path in create_connection() function

4. Run the application:
streamlit run app.py

Database setup:

-- Users table
CREATE TABLE user (
    user_id TEXT PRIMARY KEY,
    user_pass TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
);

-- Tasks table
CREATE TABLE task (
    task_id TEXT PRIMARY KEY,
    task_name TEXT NOT NULL,
    description TEXT,
    priority TEXT,
    assigned_user TEXT,
    creator TEXT,
    status TEXT DEFAULT 'new',
    FOREIGN KEY (assigned_user) REFERENCES user(user_id),
    FOREIGN KEY (creator) REFERENCES user(user_id)
);

### Usage Guide
1. Sign Up / Login
New users must create an account first
Existing users can log in with their credentials

2. Define a Task
Navigate to Define Task from sidebar
Enter task name, description, priority (1-5)
Select assignee from dropdown of all registered users
Click "Create Task" – auto-assigns Task ID

3. View Your Tasks
Go to View Tasks to see tasks assigned to you
Update status: "waiting" → "done"
Completed tasks appear with strikethrough text

4. Monitor Created Tasks
Use Check Tasks to see all tasks you created
Track which tasks are completed by assignees

5. Modify/Delete Tasks
Change Task shows only tasks you created with status 'new'
Edit name, description, or priority
Delete tasks that are no longer needed

### Navigation Flow

 Login/Sign Up
      ↓
      
 [Logged In]
      ↓
      
 ┌───────────────────────────────────┐
 │  Sidebar Navigation Options:      │
 
 │  • Define Task (Create new tasks) │
 
 │  • View Tasks (Assigned to me)    │
 
 │  • Check Tasks (Created by me)    │
 
 │  • Change Task (Modify my 'new')  │
 └───────────────────────────────────┘

  a detailed academic report covering the full project is also included.
