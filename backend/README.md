# Todo Application Backend

This is the backend for the Todo application built with FastAPI and SQLite.

## Setup and Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn main:app --reload
```

The API will be available at http://localhost:8000

## API Endpoints

- `POST /todos/` - Create a new todo
- `GET /todos/` - Get all todos (with optional filter: all/active/completed)
- `PUT /todos/{todo_id}` - Update a todo
- `DELETE /todos/{todo_id}` - Delete a todo
- `DELETE /todos/clear/completed` - Clear all completed todos
- `DELETE /todos/clear/all` - Clear all todos

## Database

The application uses SQLite as the database. The database file `todos.db` will be created automatically when you first run the application.