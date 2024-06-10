
# Electioneer Backend

This is the backend for the Electioneer application, which manages the election process, including voter registration, voting, and result tallying.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Logging](#logging)
- [License](#license)
- [File Structure](#file-structure)

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.8 or higher
- Django 3.2 or higher
- Node.js and npm (for frontend if needed)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/electioneer.git
   cd electioneer
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. **Environment Variables:**

   Create a `.env` file in the `electioneer` directory and add the following configuration settings:

   ```plaintext
   DEBUG=True
   SECRET_KEY=your_secret_key
   DATABASE_URL=sqlite:///db.sqlite3  # Update this if using a different database
   ```

## Database Setup

1. **Apply migrations to set up the database:**

   ```bash
   python manage.py migrate
   ```

2. **Create a superuser:**

   ```bash
   python manage.py createsuperuser
   ```

## Running the Application

1. **Start the development server:**

   ```bash
   python manage.py runserver
   ```

   The application will be available at `http://127.0.0.1:8000`.

## API Endpoints

Here are some of the primary API endpoints:

- **User Registration:** `POST /api/register/`
- **User Login:** `POST /api/login/`
- **Create Election:** `POST /api/elections/`
- **List Elections:** `GET /api/elections/`
- **Vote:** `POST /api/vote/`

### Example API Usage

#### Register a New User

```http
POST /api/register/
Content-Type: application/json

{
    "username": "newuser",
    "password": "newpassword",
    "email": "newuser@example.com"
}
```

#### Login

```http
POST /api/login/
Content-Type: application/json

{
    "username": "newuser",
    "password": "newpassword"
}
```

#### Create a New Election

```http
POST /api/elections/
Content-Type: application/json

{
    "name": "New Election",
    "description": "Description of the new election",
    "start_date": "2024-06-01T00:00:00Z",
    "end_date": "2024-06-30T23:59:59Z"
}
```

#### List All Elections

```http
GET /api/elections/
```

## Testing

1. **Run tests:**

   ```bash
   python manage.py test
   ```

## Logging

- Application logs can be found in `debug.log`.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## File Structure

```
backend/
├── electioneer/
│   ├── election_system/
│   ├── voters/
│   │   ├── __pycache__/
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── email_utils.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── task.py
│   │   ├── test_email.py
│   │   ├── tests.py
│   │   ├── views.py
│   ├── .env
│   ├── db.sqlite3
│   ├── debug.log
│   ├── manage.py
├── venv/
├── .gitignore
├── debug.log
├── package-lock.json
├── README.md
├── requirements.txt
```

This file structure includes the core directories for the election system and voter management, configuration files, and logs. The virtual environment (venv) is also included in the project directory but should not be pushed to the repository. Instead, it should be added to `.gitignore`.

## Usage

The main functionality of the backend includes handling file uploads, processing student data from CSV or Excel files, managing elections, and storing voting records.
```

