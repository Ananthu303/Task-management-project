
# Task Management System

A Django-based Task Management System.

---

## 🚀 Getting Started

Follow the steps below to set up and run the Task Management System on your local machine.

---

### 1. Clone the Repository

Start by cloning the project from GitHub:

```bash
git clone https://github.com/Ananthu303/Task-management-project.git
cd Task-management-project
```

### 2. Create and Activate a Virtual Environment

It is recommended to use a virtual environment to manage dependencies for this project. Here’s how to create and activate it:

For **Windows**:
```bash
python -m venv venv
venv\Scripts ctivate
```

For **macOS/Linux**:
```bash
python3 -m venv venv
source venv/bin/activate
```

Once activated, your terminal should show something like `(venv)` indicating that the virtual environment is active.

### 3. Install Dependencies

Once the virtual environment is activated, install the required dependencies listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Apply Migrations

Apply the database migrations to set up the necessary database schema:

```bash
python manage.py migrate
```

### 5. Create Superuser (Super Admin)

You need to create a superuser who will have full admin access to the system. The superuser will manage users, tasks, and system settings.

Run the following command to create the superuser:

```bash
python manage.py createsuperuser
```

You will be prompted to enter the following information:

- Username
- Email address
- Password (Make sure to choose a strong one)

This superuser is the SUPERADMIN having full control over the django admin panel and Admin dashboard of Task Management System.

### 6. Run the Development Server

Once everything is set up, run the Django development server:

```bash
python manage.py runserver
```

Now, you can access the Task Management System at `http://127.0.0.1:8000/`.

---
