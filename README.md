# ToDoTask Application

## Description

ToDoTask is a simple, intuitive to-do list application designed to help users manage their daily tasks efficiently. With
an easy-to-use interface, users can effortlessly add, edit, and delete tasks, ensuring they stay organized and focused
on their priorities.

## Installation

To set up the ToDoTask application locally, follow these steps:

1. Clone the repository:
    ```bash
    git clone 
    ```
2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Copy the given `.env` file to the root directory of the application:
4. Run the application:
    ```bash
    python app.py
    ```
5. Use the following API Endpoints to interact with the application:
    ```
    http://localhost:9999/api/auth/
    http://localhost:9999/api/v1/
    ```
6. Run the unit tests for authentication:
    ```bash
    python -m unittest test_app_auth.py
    ```
7. Run the unit tests for the service:
    ```bash
    python -m unittest test_app_v1.py
    ```
8. See the [Auth_API Endpoints](app_auth.py) and [Service_API Endpoints](app_v1.py) for more details.

# API Endpoints

## Authentication Endpoints: `/api/auth`

### `POST /register` User Registration

- Registers a new user with the application.
- Request Body:
    ```
    {
        "username": "user",
        "password": "password"
    }
    ```
- Response:
    ```
    {
        "status": "success"
    }
    ```

### `POST /login` User Login

- Authenticates an existing user with the application.
- Request Body:
    ```
    {
        "username": "user",
        "password": "password"
    }
    ```
- Response:
    ```
    {
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InVzZXIifQ.5Gzv3z"
    }
    ```
- use token for authentication in the application.

## Service Endpoints: `/api/v1`

### `GET /health` Health Check

- Returns the health status of the service.
- Response:
    ```
    {
        "status": "healthy"
    }
    ```

### `POST /add` Add Task

- Adds a new task for the authenticated user.
- Request Header:
    ```
    {
        "x-access-tokens": <token-from-login>
    }
    ```
- Request Body:
    ```
    {
        "title": "Task Title",
        "description": "Task Description",
        "done": "false",
        "time": "1609459200.0676987",
    }
    ```
- Response:
    ```
    {
        "_id": "5f9e3e3e3e3e3e3e3e3e3e3e",
    }
    ```

### `PUT /update/<todo_id>` Update Task

- Updates an existing task by ID for the authenticated user.
- Request Header:
    ```
    {
        "x-access-tokens": <token-from-login>
    }
    ```
- Request Body:
    ```
    {
        "title": "Task Title",
        "description": "Task Description",
        "done": "false",
        "time": "1609459200.0676987",
    }
    ```
- Response:
    ```
    {
        "status": "success"
    }
    ```

### `GET /get` Get All Tasks

- Retrieves all tasks for the authenticated user.
- Request Header:
    ```
    {
        "x-access-tokens": <token-from-login>
    }
    ```
- Response:
    ```
    [
        {
            "_id": "5f9e3e3e3e3e3e3e3e3e3e3e",
            "title": "Task Title",
            "description": "Task Description",
            "done": "false",
            "time": "1609459200.0676987",
        }
    ]
    ```

### `GET /get/<todo_id>` Get Task by ID

- Retrieves a specific task by ID for the authenticated user.
- Request Header:
    ```
    {
        "x-access-tokens": <token-from-login>
    }
    ```
- Response:
    ```
    {
        "_id": "5f9e3e3e3e3e3e3e3e3e3e3e",
        "title": "Task Title",
        "description": "Task Description",
        "done": "false",
        "time": "1609459200.0676987",
    }
    ```

### `DELETE /delete/<todo_id>` Delete Task

- Deletes a specific task by ID for the authenticated user.
- Request Header:
    ```
    {
        "x-access-tokens": <token-from-login>
    }
    ```
- Response:
    ```
    {
        "status": "success"
    }
    ```
