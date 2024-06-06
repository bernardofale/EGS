# To-Do API

## Overview
This To-Do API allows users to manage their to-do items with functionality for creating, reading, updating, and deleting tasks. The API requires API key authentication for all operations.

## Authentication
All routes require a valid API key. Users must create an account to receive their API key.

## User Management
### Create User
- **Endpoint**: `/v1/users`
- **Method**: `POST`
- **Description**: Creates a new user and generates an API key.
- **Request Body**:
  ```json
  {
    "username": "your_username",
    "password": "your_password"
  }
  ```

## To-Do Item Management
### Get All To-Do Items
- **Endpoint**: `/v1/todos`
- **Method**: `GET`
- **Description**: Returns a list of To-Do items with optional filters.
- **Query Parameters**:
  - `completed` (boolean): Filter by completion status (true/false).
  - `priority` (integer): Filter by priority level (1-4).
  - `due_date` (datetime): Filter by due date.
  - `sort_by_due_date` (string): Sort by due date (asc/desc).

### Get To-Do Item by ID
- **Endpoint**: `/v1/todos/{todo_id}`
- **Method**: `GET`
- **Description**: Returns a specific To-Do item based on its ID.

### Create To-Do Item
- **Endpoint**: `/v1/todos`
- **Method**: `POST`
- **Description**: Creates a new To-Do item.
- **Request Body**:
  ```json
  {
    "description": "Task description",
    "completed": false,
    "priority": 1,
    "meeting_id": "0",
    "content": "Detailed content of the task",
    "departamento_id": 1,
    "due_date": "2024-06-05T00:00:00"
  }
  ```

### Update To-Do Item
- **Endpoint**: `/v1/todos/{todo_id}`
- **Method**: `PUT`
- **Description**: Updates the parameters of a specific To-Do item based on its ID.
- **Request Body**:
  ```json
  {
    "description": "Updated task description",
    "completed": true,
    "priority": 2,
    "meeting_id": "1",
    "content": "Updated detailed content of the task",
    "departamento_id": 2,
    "due_date": "2024-06-10T00:00:00"
  }
  ```

### Delete To-Do Item
- **Endpoint**: `/v1/todos/{todo_id}`
- **Method**: `DELETE`
- **Description**: Deletes a specific To-Do item based on its ID.

## Database
The API uses SQLAlchemy with a MySQL database to store user and to-do item information.

## Running the API
The API is configured to run using Docker and Kubernetes. Ensure you have the following files set up for deployment:
- `Dockerfile`
- `docker-compose.yaml`
- `Deployment` folder containing:
  - `todo-storage-deployment.yaml`: Manages data storage for the to-do database.
  - `deployment-todo.yaml`: Includes deployments and services for both the "todo-api" and "todo-db".
  - Ingress configuration for HTTP traffic routing using Traefik.

## Testing
All endpoints were tested and confirmed to be fully functional.

To run docker:
sudo docker-compose up --build

To remove:
sudo docker volume rm $(sudo docker volume ls -qf dangling=true)
